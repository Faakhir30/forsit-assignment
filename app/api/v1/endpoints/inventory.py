from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.db.session import get_db
from app.schemas.inventory import Inventory, InventoryCreate, InventoryUpdate
from app.models.models import Inventory as InventoryModel, Product as ProductModel

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("/", response_model=List[Inventory])
def get_inventory(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all inventory items with pagination.
    """
    inventory = db.query(InventoryModel).offset(skip).limit(limit).all()
    return inventory


@router.get("/low-stock")
def get_low_stock_alerts(db: Session = Depends(get_db)):
    """
    Get products with stock levels below their threshold.
    """
    low_stock_items = (
        db.query(InventoryModel, ProductModel)
        .join(ProductModel)
        .filter(InventoryModel.quantity <= InventoryModel.low_stock_threshold)
        .all()
    )

    return [
        {
            "product_id": item.Inventory.product_id,
            "product_name": item.Product.name,
            "current_quantity": item.Inventory.quantity,
            "threshold": item.Inventory.low_stock_threshold,
        }
        for item in low_stock_items
    ]


@router.put("/{product_id}", response_model=Inventory)
def update_inventory(
    product_id: int, inventory: InventoryUpdate, db: Session = Depends(get_db)
):
    """
    Update inventory levels for a product.
    """
    db_inventory = (
        db.query(InventoryModel).filter(InventoryModel.product_id == product_id).first()
    )

    if not db_inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")

    update_data = inventory.model_dump(exclude_unset=True)
    update_data["last_updated"] = datetime.utcnow()

    for field, value in update_data.items():
        setattr(db_inventory, field, value)

    db.commit()
    db.refresh(db_inventory)
    return db_inventory


@router.get("/changes/{product_id}")
def get_inventory_changes(
    product_id: int,
    start_date: datetime = None,
    end_date: datetime = None,
    db: Session = Depends(get_db),
):
    """
    Track inventory changes over time for a specific product.
    """
    inventory = (
        db.query(InventoryModel).filter(InventoryModel.product_id == product_id).first()
    )

    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")

    query = db.query(
        ProductModel.name, InventoryModel.quantity, InventoryModel.last_updated
    ).join(ProductModel)

    if start_date:
        query = query.filter(InventoryModel.last_updated >= start_date)
    if end_date:
        query = query.filter(InventoryModel.last_updated <= end_date)

    changes = query.order_by(InventoryModel.last_updated.desc()).all()

    return {
        "product_id": product_id,
        "changes": [
            {"product_name": name, "quantity": quantity, "updated_at": updated}
            for name, quantity, updated in changes
        ],
    }
