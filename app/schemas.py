from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class OrderCreate(BaseModel):
    order_id: str = Field(min_length=1, max_length=100)
    sku: str = Field(min_length=1, max_length=100)
    expected_qty: int = Field(ge=0)


class WarehouseRecordCreate(BaseModel):
    order_id: str = Field(min_length=1, max_length=100)
    sku: str = Field(min_length=1, max_length=100)
    actual_qty: int


class ResolveRequest(BaseModel):
    note: str = Field(min_length=3, max_length=1000)


class ReviewRequest(BaseModel):
    approved: bool
    note: str | None = Field(default=None, max_length=1000)


class AIClassification(BaseModel):
    classification: Literal[
        "negative_inventory",
        "supplier_shortage",
        "warehouse_shortage",
        "probable_return_mismatch",
        "overstock",
        "unknown",
    ]
    confidence: float = Field(ge=0, le=1)
    recommended_action: str = Field(min_length=3, max_length=1000)
    requires_human_review: bool


class ExceptionOut(BaseModel):
    id: int
    order_id: str
    sku: str
    expected_qty: int
    actual_qty: int
    difference: int
    exception_type: str
    severity: str
    status: str
    resolution_note: str | None
    created_at: datetime
    model_config = {"from_attributes": True}


class AutomationJobCreate(BaseModel):
    external_job_id: str = Field(min_length=1, max_length=100)
    exception_id: int = Field(gt=0)
