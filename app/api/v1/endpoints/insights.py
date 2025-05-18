from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.db.session import get_db
from app.models.models import Sale, Product, Inventory

router = APIRouter(prefix="/insights", tags=["insights"])


@router.get("/sales-trends")
async def get_sales_trends(days: int = 7, db: Session = Depends(get_db)):
    """Shows sales trends over the past week."""
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)

    # Daily sales for the period
    daily_sales = (
        db.query(
            func.date(Sale.sale_date).label("date"),
            func.sum(Sale.total_amount).label("total_sales"),
            func.count(Sale.id).label("num_orders"),
        )
        .filter(Sale.sale_date >= start_date)
        .group_by(func.date(Sale.sale_date))
        .order_by(func.date(Sale.sale_date))
        .all()
    )

    return {
        "period": f"Last {days} days",
        "daily_breakdown": [
            {
                "date": date.strftime("%Y-%m-%d"),
                "sales": float(sales),
                "orders": int(orders),
            }
            for date, sales, orders in daily_sales
        ],
    }


@router.get("/category-performance")
async def get_category_performance(db: Session = Depends(get_db)):
    """Shows how different product categories are performing."""
    last_30_days = datetime.utcnow() - timedelta(days=30)

    category_stats = (
        db.query(
            Product.category,
            func.count(Sale.id).label("total_orders"),
            func.sum(Sale.total_amount).label("total_revenue"),
        )
        .join(Sale)
        .filter(Sale.sale_date >= last_30_days)
        .group_by(Product.category)
        .all()
    )

    return [
        {
            "category": cat,
            "orders": int(orders),
            "revenue": float(rev),
            "avg_order_value": round(float(rev) / int(orders), 2) if orders > 0 else 0,
        }
        for cat, orders, rev in category_stats
    ]


@router.get("/stock-management")
async def get_stock_insights(db: Session = Depends(get_db)):
    """Helps with inventory management decisions."""
    # Get products with their sales velocity
    stock_insights = (
        db.query(
            Product.name,
            Product.category,
            Inventory.quantity,
            Inventory.low_stock_threshold,
            func.count(Sale.id).label("monthly_sales"),
        )
        .join(Inventory)
        .outerjoin(Sale, Sale.sale_date >= datetime.utcnow() - timedelta(days=30))
        .group_by(Product.id)
        .all()
    )

    return [
        {
            "product": name,
            "category": category,
            "current_stock": quantity,
            "monthly_sales": int(sales),
            "status": "Low" if quantity <= low_stock_threshold else "Good",
            "estimated_days_left": (
                round(quantity / (sales / 30), 1) if sales > 0 else "∞"
            ),
        }
        for name, category, quantity, low_stock_threshold, sales in stock_insights
    ]
