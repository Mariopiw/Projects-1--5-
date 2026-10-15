from datetime import datetime, timedelta

from celery.utils.log import get_task_logger
from sqlalchemy import select

from app.db import SessionLocal
from app.integrations.legacy_portal import LegacyPortalClient
from app.models import AutomationJob, ExceptionRecord, ExceptionStatus, JobStatus
from app.services.audit import write_audit
from app.tasks.celery_app import celery_app

logger = get_task_logger(__name__)


@celery_app.task(bind=True, max_retries=4, name="app.tasks.jobs.run_automation_job")
def run_automation_job(self, job_id: int):
    db = SessionLocal()
    try:
        job = db.get(AutomationJob, job_id)
        if job is None or job.status == JobStatus.COMPLETED:
            return
        job.status = JobStatus.RUNNING
        write_audit(db, "automation_job", job.id, "job_started", "worker")
        db.commit()

        exception = db.get(ExceptionRecord, job.exception_id)
        portal = LegacyPortalClient().fetch_order(exception.order_id)
        job.portal_status = portal.status
        job.portal_quantity = portal.quantity
        job.status = JobStatus.COMPLETED
        job.completed_at = datetime.utcnow()
        write_audit(db, "automation_job", job.id, "portal_read_verified", "worker", f"status={portal.status}; quantity={portal.quantity}")
        db.commit()
    except Exception as exc:
        db.rollback()
        logger.exception("automation job failed")
        try:
            job = db.get(AutomationJob, job_id)
            if job:
                job.status = JobStatus.FAILED
                job.error_message = str(exc)
                write_audit(db, "automation_job", job.id, "job_failed", "worker", str(exc))
                db.commit()
        finally:
            if self.request.retries < self.max_retries:
                raise self.retry(exc=exc, countdown=min(30 * (2 ** self.request.retries), 300))
            raise
    finally:
        db.close()


@celery_app.task(name="app.tasks.jobs.escalate_open_exceptions")
def escalate_open_exceptions():
    db = SessionLocal()
    try:
        cutoff = datetime.utcnow() - timedelta(minutes=15)
        records = db.scalars(
            select(ExceptionRecord).where(
                ExceptionRecord.status == ExceptionStatus.OPEN,
                ExceptionRecord.severity.in_(["critical", "high"]),
                ExceptionRecord.created_at <= cutoff,
            )
        ).all()
        for record in records:
            record.status = ExceptionStatus.ESCALATED
            write_audit(db, "exception", record.id, "exception_escalated", "scheduler")
        db.commit()
    finally:
        db.close()
