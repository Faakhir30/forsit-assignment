from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SaleBase(BaseModel):
    product_id: int
    quantity: int
    total_amount: float
    sale_date: datetime


class SaleCreate(SaleBase):
    pass


class SaleUpdate(SaleBase):
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    total_amount: Optional[float] = None
    sale_date: Optional[datetime] = None


class Sale(SaleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
