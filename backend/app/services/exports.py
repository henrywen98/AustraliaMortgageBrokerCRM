import os
import sqlite3
import secrets
from pathlib import Path
from datetime import datetime
from typing import Tuple

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from sqlmodel import Session, select

from app.models import ExportJob, Deal, Client


def _create_sqlite_view(tmp_path: Path, db: Session) -> int:
    conn = sqlite3.connect(tmp_path)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE deals_masked (
            id INTEGER PRIMARY KEY,
            client_name TEXT,
            lender TEXT,
            loan_type TEXT,
            amount REAL,
            stage TEXT,
            due_date TEXT
        )
        """
    )
    rows = 0
    for deal, client in db.exec(
        select(Deal, Client).where(Deal.client_id == Client.id)
    ):
        cur.execute(
            "INSERT INTO deals_masked(id, client_name, lender, loan_type, amount, stage, due_date) VALUES (?,?,?,?,?,?,?)",
            (
                deal.id,
                client.name,
                deal.lender,
                deal.loan_type,
                float(deal.amount or 0),
                deal.stage.value,
                deal.due_date.isoformat() if deal.due_date else None,
            ),
        )
        rows += 1
    conn.commit()
    conn.close()
    return rows


def _encrypt_bytes(data: bytes, key: bytes) -> Tuple[bytes, bytes]:
    """Return (nonce, ciphertext) using AES-256-GCM"""
    aesgcm = AESGCM(key)
    nonce = secrets.token_bytes(12)
    ct = aesgcm.encrypt(nonce, data, None)
    return nonce, ct


def run_export(db: Session, exports_dir: Path, aes_key: bytes) -> ExportJob:
    exports_dir.mkdir(parents=True, exist_ok=True)
    job = ExportJob(status="running")
    db.add(job)
    db.commit()
    db.refresh(job)

    tmp_sqlite = exports_dir / f"export_{job.id}.sqlite"
    out_file = exports_dir / f"export_{job.id}.enc"
    try:
        rows = _create_sqlite_view(tmp_sqlite, db)
        with open(tmp_sqlite, "rb") as f:
            data = f.read()
        nonce, ct = _encrypt_bytes(data, aes_key)
        with open(out_file, "wb") as f:
            f.write(nonce + ct)
        job.status = "success"
        job.file_uri = str(out_file)
        job.rows_count = rows
    except Exception:
        job.status = "failed"
        raise
    finally:
        if tmp_sqlite.exists():
            try:
                tmp_sqlite.unlink()
            except Exception:
                pass
        job.finished_at = datetime.utcnow()
        db.add(job)
        db.commit()
        db.refresh(job)
    return job

