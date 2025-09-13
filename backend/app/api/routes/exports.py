from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from pathlib import Path
import binascii

from app.api.deps import get_db, require_roles
from app.core.config import settings
from app.models import ExportJob, UserRole
from app.services.exports import run_export


router = APIRouter()


EXPORT_DIR = Path("/data/exports")


@router.post("/run", response_model=dict)
def run(db: Session = Depends(get_db), user=Depends(require_roles(UserRole.Admin))):
    if not settings.AES_KEY_HEX or len(settings.AES_KEY_HEX) != 64:
        raise HTTPException(status_code=400, detail="AES_KEY_HEX not set or invalid (need 64 hex chars)")
    aes_key = binascii.unhexlify(settings.AES_KEY_HEX)
    job = run_export(db, EXPORT_DIR, aes_key)
    return {"id": job.id, "status": job.status}


@router.get("/", response_model=list[dict])
def list_jobs(db: Session = Depends(get_db), user=Depends(require_roles(UserRole.Admin))):
    jobs = db.exec(select(ExportJob).order_by(ExportJob.id.desc())).all()
    return [
        {
            "id": j.id,
            "status": j.status,
            "file_uri": j.file_uri,
            "rows_count": j.rows_count,
            "started_at": j.started_at,
            "finished_at": j.finished_at,
        }
        for j in jobs
    ]


@router.get("/{job_id}/download")
def download(job_id: int, db: Session = Depends(get_db), user=Depends(require_roles(UserRole.Admin))):
    j = db.get(ExportJob, job_id)
    if not j or not j.file_uri:
        raise HTTPException(status_code=404, detail="Not found")
    p = Path(j.file_uri)
    if not p.exists():
        raise HTTPException(status_code=404, detail="File missing")
    return FileResponse(str(p), filename=p.name, media_type="application/octet-stream")

