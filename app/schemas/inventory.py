from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class InventoryBase(BaseModel):
    product_id: int
    quantity: int
    low_stock_threshold: int = 10
    last_updated: datetime


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(InventoryBase):
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    low_stock_threshold: Optional[int] = None
    last_updated: Optional[datetime] = None


class Inventory(InventoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
