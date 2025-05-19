# E-commerce Admin API

This is a FastAPI-based backend API for an e-commerce admin dashboard that provides insights into sales, revenue, and inventory management.

## Features

- Sales Status Analysis
  - Retrieve and filter sales data
  - Analyze revenue (daily/weekly/monthly/annual)
  - Compare revenue across periods and categories
  - Filter sales by date range, product, and category

- Inventory Management
  - View current inventory status
  - Low stock alerts
  - Inventory level updates
  - Track inventory changes

## Tech Stack

- Python 3.8+
- FastAPI
- MySQL
- SQLAlchemy
- Alembic (for database migrations)

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd e-commerce-admin-api
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with the following content:
   ```
   DATABASE_URL=mysql://user:password@localhost/ecommerce_admin
   SECRET_KEY=your-secret-key
   ```

5. Create the database:
   ```bash
   mysql -u root -p
   CREATE DATABASE ecommerce_admin;
   ```

6. Run database migrations:
   ```bash
   alembic upgrade head
   ```

7. Load demo data:
   ```bash
   python scripts/load_demo_data.py
   ```

8. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

Detailed OpenAPI Documentation:

## API Documentation
The API is fully documented using OpenAPI/Swagger, accessible at `/docs` endpoint.

Once the server is running, you can access:
- Interactive API documentation: http://localhost:8000/docs
![OpenAPI Documentation](./openapi_docs.png)
- Alternative API documentation: http://localhost:8000/redoc
![API Documentation](./docs.png)

### Main Endpoints

#### Sales Endpoints
- `GET /api/v1/sales/` - Get all sales
- `GET /api/v1/sales/analytics` - Get sales analytics
- `GET /api/v1/sales/revenue` - Get revenue analysis
- `GET /api/v1/sales/comparison` - Compare sales across periods

#### Inventory Endpoints
- `GET /api/v1/inventory/` - Get current inventory status
- `GET /api/v1/inventory/low-stock` - Get low stock alerts
- `PUT /api/v1/inventory/{product_id}` - Update inventory levels

#### Product Endpoints
- `GET /api/v1/products/` - List all products
- `POST /api/v1/products/` - Register new product
- `GET /api/v1/products/{product_id}` - Get product details
- `PUT /api/v1/products/{product_id}` - Update product

## Database Schema

### Products Table
- id (Primary Key)
- name
- description
- category
- price
- created_at
- updated_at

### Sales Table
- id (Primary Key)
- product_id (Foreign Key)
- quantity
- total_amount
- sale_date
- created_at

### Inventory Table
- id (Primary Key)
- product_id (Foreign Key)
- quantity
- low_stock_threshold
- last_updated
- created_at

## License

MIT License 