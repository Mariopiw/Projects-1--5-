from sqlalchemy.orm import Session

from app.models import AuditLog


def write_audit(db: Session, entity_type: str, entity_id: int, action: str, actor: str, details: str | None = None) -> None:
    db.add(AuditLog(entity_type=entity_type, entity_id=entity_id, action=action, actor=actor, details=details))
