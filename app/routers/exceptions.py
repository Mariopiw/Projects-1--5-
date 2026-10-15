from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models import AuditLog, ExceptionRecord, ExceptionStatus, TriageDecision, User
from app.schemas import ExceptionOut, ResolveRequest, ReviewRequest
from app.security import require_roles
from app.services.audit import write_audit

router = APIRouter(prefix="/exceptions", tags=["exceptions"])


@router.get("", response_model=list[ExceptionOut])
def list_exceptions(status_value: str | None = Query(default=None, alias="status"), severity: str | None = None, db: Session = Depends(get_db), user: User = Depends(require_roles("viewer", "operator", "admin"))):
    stmt = select(ExceptionRecord)
    if status_value:
        stmt = stmt.where(ExceptionRecord.status == status_value)
    if severity:
        stmt = stmt.where(ExceptionRecord.severity == severity)
    return list(db.scalars(stmt.order_by(ExceptionRecord.created_at.desc())).all())


@router.post("/{exception_id}/acknowledge", response_model=ExceptionOut)
def acknowledge(exception_id: int, db: Session = Depends(get_db), user: User = Depends(require_roles("operator", "admin"))):
    record = db.get(ExceptionRecord, exception_id)
    if record is None:
        raise HTTPException(404, "Exception not found")
    if record.status == ExceptionStatus.RESOLVED:
        raise HTTPException(409, "Resolved exception cannot be acknowledged")
    record.status = ExceptionStatus.ACKNOWLEDGED
    record.acknowledged_by = user.username
    record.acknowledged_at = datetime.utcnow()
    write_audit(db, "exception", record.id, "exception_acknowledged", user.username)
    db.commit(); db.refresh(record)
    return record


@router.post("/{exception_id}/resolve", response_model=ExceptionOut)
def resolve(exception_id: int, payload: ResolveRequest, db: Session = Depends(get_db), user: User = Depends(require_roles("operator", "admin"))):
    record = db.get(ExceptionRecord, exception_id)
    if record is None:
        raise HTTPException(404, "Exception not found")
    record.status = ExceptionStatus.RESOLVED
    record.resolution_note = payload.note
    record.resolved_at = datetime.utcnow()
    write_audit(db, "exception", record.id, "exception_resolved", user.username, payload.note)
    db.commit(); db.refresh(record)
    return record


@router.post("/{exception_id}/triage/{decision_id}/review")
def review_triage(exception_id: int, decision_id: int, payload: ReviewRequest, db: Session = Depends(get_db), user: User = Depends(require_roles("operator", "admin"))):
    decision = db.get(TriageDecision, decision_id)
    if decision is None or decision.exception_id != exception_id:
        raise HTTPException(404, "Triage decision not found")
    if decision.approved is not None:
        raise HTTPException(409, "Decision already reviewed")
    decision.approved = payload.approved
    decision.approved_by = user.username
    write_audit(db, "exception", exception_id, "triage_reviewed", user.username, payload.note)
    db.commit()
    return {"decision_id": decision.id, "approved": decision.approved}


@router.get("/{exception_id}/audit")
def audit(exception_id: int, db: Session = Depends(get_db), user: User = Depends(require_roles("viewer", "operator", "admin"))):
    logs = db.scalars(select(AuditLog).where(AuditLog.entity_type == "exception", AuditLog.entity_id == exception_id).order_by(AuditLog.created_at)).all()
    return [{"action": x.action, "actor": x.actor, "details": x.details, "created_at": x.created_at} for x in logs]
