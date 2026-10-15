from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models import AutomationJob, ExceptionRecord, User
from app.schemas import AutomationJobCreate
from app.security import require_roles
from app.services.audit import write_audit
from app.tasks.jobs import run_automation_job

router = APIRouter(prefix="/jobs", tags=["automation"] )


@router.post("", status_code=201)
def create_job(payload: AutomationJobCreate, db: Session = Depends(get_db), user: User = Depends(require_roles("operator", "admin"))):
    if db.get(ExceptionRecord, payload.exception_id) is None:
        raise HTTPException(404, "Exception not found")
    job = AutomationJob(external_job_id=payload.external_job_id, exception_id=payload.exception_id)
    db.add(job)
    try:
        db.flush(); write_audit(db, "automation_job", job.id, "job_created", user.username); db.commit(); db.refresh(job)
    except IntegrityError:
        db.rollback(); existing = db.scalar(select(AutomationJob).where(AutomationJob.external_job_id == payload.external_job_id)); return {"message": "Already exists", "job_id": existing.id}
    return {"job_id": job.id, "status": job.status}


@router.post("/{job_id}/run", status_code=202)
def run_job(job_id: int, db: Session = Depends(get_db), user: User = Depends(require_roles("operator", "admin"))):
    job = db.get(AutomationJob, job_id)
    if job is None:
        raise HTTPException(404, "Job not found")
    run_automation_job.delay(job.id)
    return {"message": "Accepted", "job_id": job.id}


@router.get("")
def list_jobs(db: Session = Depends(get_db), user: User = Depends(require_roles("viewer", "operator", "admin"))):
    return list(db.scalars(select(AutomationJob).order_by(AutomationJob.created_at.desc())).all())
