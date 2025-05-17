from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from .base import Base, BaseModel


class Product(Base, BaseModel):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)

    # Relationships
    sales = relationship("Sale", back_populates="product")
    inventory = relationship("Inventory", back_populates="product", uselist=False)


class Sale(Base, BaseModel):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)
    sale_date = Column(DateTime, nullable=False)

    # Relationships
    product = relationship("Product", back_populates="sales")


class Inventory(Base, BaseModel):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), unique=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    low_stock_threshold = Column(Integer, nullable=False, default=10)
    last_updated = Column(DateTime, nullable=False)

    # Relationships
    product = relationship("Product", back_populates="inventory")
