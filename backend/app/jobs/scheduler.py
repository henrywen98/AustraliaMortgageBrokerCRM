from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlmodel import Session
from pathlib import Path
import binascii

from app.core.config import settings
from app.db.session import engine
from app.services.exports import run_export


def start_scheduler():
    if not settings.AES_KEY_HEX or len(settings.AES_KEY_HEX) != 64:
        return None  # no key -> skip scheduling
    scheduler = BackgroundScheduler(timezone="Australia/Sydney")

    def export_job():
        with Session(engine) as db:
            key = binascii.unhexlify(settings.AES_KEY_HEX)
            run_export(db, Path("/data/exports"), key)

    # Every 2 hours
    scheduler.add_job(export_job, CronTrigger(minute=0, hour="*/2"))
    scheduler.start()
    return scheduler

