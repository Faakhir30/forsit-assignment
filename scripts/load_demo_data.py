import sys
import os
from datetime import datetime, timedelta
import random

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.models import Product, Sale, Inventory

# Sample product data
PRODUCTS = [
    {
        "name": "Amazon Echo Dot (4th Gen)",
        "description": "Smart speaker with Alexa",
        "category": "Smart Home",
        "price": 49.99,
    },
    {
        "name": "Walmart Basics Microwave",
        "description": "700W Countertop Microwave Oven",
        "category": "Appliances",
        "price": 69.99,
    },
    {
        "name": "Amazon Fire TV Stick 4K",
        "description": "Streaming media player",
        "category": "Electronics",
        "price": 39.99,
    },
    {
        "name": "Walmart Mainstays Office Chair",
        "description": "Ergonomic desk chair",
        "category": "Furniture",
        "price": 89.99,
    },
    {
        "name": "Amazon Kindle Paperwhite",
        "description": "E-reader with backlight",
        "category": "Electronics",
        "price": 129.99,
    },
]


def create_demo_data():
    db = SessionLocal()
    try:
        # Create products
        products = []
        for product_data in PRODUCTS:
            product = Product(**product_data)
            db.add(product)
            products.append(product)
        db.commit()

        # Create inventory records
        for product in products:
            inventory = Inventory(
                product_id=product.id,
                quantity=random.randint(10, 100),
                low_stock_threshold=20,
                last_updated=datetime.utcnow(),
            )
            db.add(inventory)
        db.commit()

        # Create sales records (last 30 days)
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)

        for _ in range(100):  # Create 100 random sales
            sale_date = start_date + timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
            )

            product = random.choice(products)
            quantity = random.randint(1, 5)

            sale = Sale(
                product_id=product.id,
                quantity=quantity,
                total_amount=product.price * quantity,
                sale_date=sale_date,
            )
            db.add(sale)

        db.commit()
        print("Demo data created successfully!")

    except Exception as e:
        print(f"Error creating demo data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_demo_data()
