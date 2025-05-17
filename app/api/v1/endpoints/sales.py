from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict
from datetime import datetime, timedelta
from app.db.session import get_db
from app.schemas.sale import Sale, SaleCreate, SaleUpdate
from app.models.models import Sale as SaleModel, Product as ProductModel

router = APIRouter(prefix="/sales", tags=["sales"])


@router.get("/", response_model=List[Sale])
def get_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all sales with pagination.
    """
    sales = db.query(SaleModel).offset(skip).limit(limit).all()
    return sales


@router.post("/", response_model=Sale)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    """
    Create a new sale record.
    """
    db_sale = SaleModel(**sale.model_dump())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale


@router.get("/analytics")
def get_sales_analytics(
    start_date: datetime = None,
    end_date: datetime = None,
    db: Session = Depends(get_db),
):
    """
    Get sales analytics including total revenue and number of sales.
    """
    query = db.query(SaleModel)

    if start_date:
        query = query.filter(SaleModel.sale_date >= start_date)
    if end_date:
        query = query.filter(SaleModel.sale_date <= end_date)

    total_revenue = query.with_entities(func.sum(SaleModel.total_amount)).scalar() or 0

    total_sales = query.count()

    return {
        "total_revenue": float(total_revenue),
        "total_sales": total_sales,
        "average_order_value": (
            float(total_revenue / total_sales) if total_sales > 0 else 0
        ),
    }


@router.get("/revenue/comparison")
def compare_revenue(period: str = "daily", db: Session = Depends(get_db)):
    """
    Compare revenue across different periods (daily, weekly, monthly, annual).
    """
    today = datetime.utcnow()

    if period == "daily":
        current_start = today.replace(hour=0, minute=0, second=0, microsecond=0)
        previous_start = current_start - timedelta(days=1)
    elif period == "weekly":
        current_start = today - timedelta(days=today.weekday())
        previous_start = current_start - timedelta(weeks=1)
    elif period == "monthly":
        current_start = today.replace(day=1)
        previous_start = (current_start - timedelta(days=1)).replace(day=1)
    else:  # annual
        current_start = today.replace(month=1, day=1)
        previous_start = current_start.replace(year=current_start.year - 1)

    current_revenue = (
        db.query(func.sum(SaleModel.total_amount))
        .filter(SaleModel.sale_date >= current_start)
        .scalar()
        or 0
    )

    previous_revenue = (
        db.query(func.sum(SaleModel.total_amount))
        .filter(
            SaleModel.sale_date >= previous_start, SaleModel.sale_date < current_start
        )
        .scalar()
        or 0
    )

    return {
        "period": period,
        "current_revenue": float(current_revenue),
        "previous_revenue": float(previous_revenue),
        "change_percentage": (
            ((current_revenue - previous_revenue) / previous_revenue * 100)
            if previous_revenue > 0
            else 0
        ),
    }


@router.get("/by-category")
def get_sales_by_category(
    start_date: datetime = None,
    end_date: datetime = None,
    db: Session = Depends(get_db),
):
    """
    Get sales data grouped by product category.
    """
    query = db.query(
        ProductModel.category,
        func.sum(SaleModel.total_amount).label("total_revenue"),
        func.count(SaleModel.id).label("total_sales"),
    ).join(ProductModel)

    if start_date:
        query = query.filter(SaleModel.sale_date >= start_date)
    if end_date:
        query = query.filter(SaleModel.sale_date <= end_date)

    results = query.group_by(ProductModel.category).all()

    return [
        {
            "category": category,
            "total_revenue": float(total_revenue),
            "total_sales": total_sales,
        }
        for category, total_revenue, total_sales in results
    ]
