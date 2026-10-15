from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models import ExceptionRecord, Order, TriageDecision, User, WarehouseRecord
from app.schemas import OrderCreate, WarehouseRecordCreate
from app.security import require_roles
from app.services.audit import write_audit
from app.services.reconciliation import classify_difference
from app.services.triage import triage

router = APIRouter(tags=["orders"] )


@router.post("/orders", status_code=201)
def create_order(payload: OrderCreate, db: Session = Depends(get_db), user: User = Depends(require_roles("operator", "admin"))):
    order = Order(**payload.model_dump())
    db.add(order)
    try:
        db.commit(); db.refresh(order)
    except IntegrityError as exc:
        db.rollback(); raise HTTPException(status_code=409, detail="Order already exists") from exc
    return {"id": order.id, **payload.model_dump()}


@router.post("/warehouse-records", status_code=201)
def create_warehouse_record(payload: WarehouseRecordCreate, db: Session = Depends(get_db), user: User = Depends(require_roles("operator", "admin"))):
    record = WarehouseRecord(**payload.model_dump())
    db.add(record)
    try:
        db.commit(); db.refresh(record)
    except IntegrityError as exc:
        db.rollback(); raise HTTPException(status_code=409, detail="Warehouse record already exists") from exc
    return {"id": record.id, **payload.model_dump()}


@router.post("/reconciliation/run")
def run_reconciliation(db: Session = Depends(get_db), user: User = Depends(require_roles("operator", "admin"))):
    orders = list(db.scalars(select(Order)).all())
    wh = {(r.order_id, r.sku): r for r in db.scalars(select(WarehouseRecord)).all()}
    created = matched = 0
    for order in orders:
        actual = wh.get((order.order_id, order.sku)).actual_qty if (order.order_id, order.sku) in wh else 0
        cls = classify_difference(order.expected_qty, actual)
        if cls.exception_type == "match":
            matched += 1; continue
        existing = db.scalar(select(ExceptionRecord).where(ExceptionRecord.order_id == order.order_id, ExceptionRecord.sku == order.sku))
        if existing:
            continue
        exc = ExceptionRecord(order_id=order.order_id, sku=order.sku, expected_qty=order.expected_qty, actual_qty=actual, difference=actual-order.expected_qty, exception_type=cls.exception_type, severity=cls.severity)
        db.add(exc); db.flush()
        source, decision = triage(cls.exception_type, cls.severity, exc.difference)
        db.add(TriageDecision(exception_id=exc.id, source=source, classification=decision.classification, confidence=decision.confidence, recommended_action=decision.recommended_action, requires_human_review=decision.requires_human_review))
        write_audit(db, "exception", exc.id, "exception_created", user.username, f"severity={cls.severity}")
        created += 1
    db.commit()
    return {"checked": len(orders), "matched": matched, "exceptions_created": created}
