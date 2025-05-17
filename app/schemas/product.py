from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    price: float = Field(gt=0)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = Field(gt=0, default=None)


class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
