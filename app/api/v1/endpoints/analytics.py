from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime, timedelta
import asyncio
from app.db.session import get_db
from app.models.models import Sale, Product, Inventory

router = APIRouter(prefix="/analytics", tags=["analytics"])


# Simple manager to handle active dashboard connections
class AnalyticsManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, data: dict):
        for connection in self.active_connections:
            await connection.send_json(data)


analytics_manager = AnalyticsManager()


async def get_business_metrics(db: Session) -> dict:
    """Gets key business metrics for the dashboard."""
    now = datetime.utcnow()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = today - timedelta(days=1)

    # Today's total sales
    today_sales = (
        db.query(func.sum(Sale.total_amount)).filter(Sale.sale_date >= today).scalar()
        or 0
    )

    # Yesterday's sales for comparison
    yesterday_sales = (
        db.query(func.sum(Sale.total_amount))
        .filter(Sale.sale_date >= yesterday, Sale.sale_date < today)
        .scalar()
        or 0
    )

    # Products running low on stock
    low_stock = (
        db.query(Inventory, Product)
        .join(Product)
        .filter(Inventory.quantity <= Inventory.low_stock_threshold)
        .all()
    )

    # Best sellers today
    top_sellers = (
        db.query(
            Product.name,
            func.sum(Sale.quantity).label("units_sold"),
            func.sum(Sale.total_amount).label("revenue"),
        )
        .join(Sale)
        .filter(Sale.sale_date >= today)
        .group_by(Product.name)
        .order_by(func.sum(Sale.total_amount).desc())
        .limit(5)
        .all()
    )

    return {
        "updated_at": now.strftime("%Y-%m-%d %H:%M:%S"),
        "daily_snapshot": {
            "today_sales": float(today_sales),
            "yesterday_sales": float(yesterday_sales),
            "growth": round(
                (
                    (today_sales - yesterday_sales) / yesterday_sales * 100
                    if yesterday_sales > 0
                    else 0
                ),
                1,
            ),
        },
        "inventory_alerts": [
            {
                "product": item.Product.name,
                "current_stock": item.Inventory.quantity,
                "min_required": item.Inventory.low_stock_threshold,
            }
            for item in low_stock
        ],
        "top_performers": [
            {"product": name, "units_sold": int(units), "revenue": float(rev)}
            for name, units, rev in top_sellers
        ],
    }


async def dashboard_update_task():
    """Background task to update dashboard metrics periodically"""
    while True:
        try:
            db = next(get_db())
            metrics = await get_business_metrics(db)
            await analytics_manager.broadcast(metrics)
        except Exception as e:
            print(f"Error updating dashboard: {e}")
        finally:
            db.close()
        await asyncio.sleep(30)  # Update every 30 seconds


@router.websocket("/ws/dashboard")
async def dashboard_websocket(websocket: WebSocket, db: Session = Depends(get_db)):
    """WebSocket endpoint for real-time dashboard updates"""
    await analytics_manager.connect(websocket)
    try:
        # Send initial metrics
        metrics = await get_business_metrics(db)
        await websocket.send_json(metrics)

        # Keep connection alive and handle disconnection
        while True:
            try:
                # Wait for any client message (ping/pong)
                await websocket.receive_text()
            except WebSocketDisconnect:
                break
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        analytics_manager.disconnect(websocket)


# Register startup event handler
async def start_dashboard_updates():
    asyncio.create_task(dashboard_update_task())


router.add_event_handler("startup", start_dashboard_updates)


@router.get("/snapshot")
async def get_current_snapshot(db: Session = Depends(get_db)):
    """Quick snapshot of current business metrics."""
    return await get_business_metrics(db)
