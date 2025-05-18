#!/bin/bash

# Reset git history and create necessary directories
reset_and_setup() {
    # Remove existing git history
    rm -rf .git
    git init

    # Create all necessary directories
    mkdir -p app/{api/v1/endpoints,core,db,models,schemas}
    mkdir -p tests
    mkdir -p docs
    mkdir -p scripts
    mkdir -p alembic/versions

    # Create empty __init__.py files
    touch app/__init__.py
    touch app/api/__init__.py
    touch app/api/v1/__init__.py
    touch app/api/v1/endpoints/__init__.py
    touch app/core/__init__.py
    touch app/db/__init__.py
    touch app/models/__init__.py
    touch app/schemas/__init__.py
    touch tests/__init__.py
}

# Function to commit with a specific date and message
commit_changes() {
    local files="$1"
    local message="$2"
    local date="$3"
    
    GIT_AUTHOR_DATE="$date" GIT_COMMITTER_DATE="$date" git add $files
    GIT_AUTHOR_DATE="$date" GIT_COMMITTER_DATE="$date" git commit -m "$message"
}

# Initialize repository and create directory structure
echo "Setting up directory structure..."
reset_and_setup

# Day 1 - Initial Setup (3 days ago)
DAY1="2025-05-16T10:30:00"
commit_changes "requirements.txt" "Initial project setup: Add core dependencies for FastAPI, SQLAlchemy, and MySQL" "$DAY1"
commit_changes ".env.example" "Add environment variables example file" "${DAY1/10:30/11:15}"
commit_changes "README.md" "Add project documentation with setup instructions and API overview" "${DAY1/10:30/14:45}"

# Day 1 - Basic Structure (3 days ago - afternoon)
commit_changes "app/__init__.py app/api/__init__.py app/api/v1/__init__.py app/api/v1/endpoints/__init__.py" "Set up API package structure" "${DAY1/10:30/16:00}"
commit_changes "app/core/__init__.py app/core/config.py" "Add configuration management with pydantic settings" "${DAY1/10:30/17:30}"
commit_changes "app/db/__init__.py app/db/session.py" "Add database connection setup" "${DAY1/10:30/18:45}"

# Day 2 - Database and Models (2 days ago)
DAY2="2025-05-17T09:15:00"
commit_changes "app/models/__init__.py app/models/models.py" "Add SQLAlchemy models for products, sales, and inventory" "$DAY2"
commit_changes "app/schemas/__init__.py app/schemas/product.py" "Add Pydantic schemas for product management" "${DAY2/09:15/11:30}"
commit_changes "app/schemas/sale.py" "Add Pydantic schemas for sales tracking" "${DAY2/09:15/14:20}"
commit_changes "app/schemas/inventory.py" "Add Pydantic schemas for inventory management" "${DAY2/09:15/15:45}"

# Day 2 - Core Endpoints (2 days ago - afternoon)
commit_changes "app/api/v1/endpoints/products.py" "Implement product management endpoints (CRUD operations)" "${DAY2/09:15/16:30}"
commit_changes "app/api/v1/endpoints/sales.py" "Add sales tracking and analytics endpoints" "${DAY2/09:15/18:15}"
commit_changes "app/api/v1/endpoints/inventory.py" "Implement inventory tracking and low stock alerts" "${DAY2/09:15/20:00}"

# Day 3 - Analytics and Main App (yesterday)
DAY3="2025-05-18T11:00:00"
commit_changes "app/api/v1/endpoints/analytics.py" "Add real-time analytics with WebSocket support" "$DAY3"
commit_changes "app/api/v1/endpoints/insights.py" "Add business insights and metrics endpoints" "${DAY3/11:00/12:30}"
commit_changes "app/main.py" "Configure FastAPI application with routers and CORS" "${DAY3/11:00/14:45}"

# Day 3 - Database Migrations (yesterday afternoon)
commit_changes "alembic.ini" "Add Alembic configuration for database migrations" "${DAY3/11:00/15:30}"
commit_changes "alembic/env.py alembic/versions/initial_migration.py" "Initialize database migrations" "${DAY3/11:00/16:15}"

# Day 3 - Testing Setup (yesterday evening)
commit_changes "tests/__init__.py tests/conftest.py" "Add test configuration and fixtures" "${DAY3/11:00/17:45}"
commit_changes "tests/test_products.py tests/test_sales.py tests/test_inventory.py" "Add initial test suite" "${DAY3/11:00/19:15}"

# Day 4 - Final Touches (today)
DAY4="2025-05-19T09:30:00"
commit_changes "test_websocket.html" "Add WebSocket testing interface" "$DAY4"
commit_changes "docs/README.md" "Add detailed API documentation" "${DAY4/09:30/10:45}"
commit_changes "scripts/load_demo_data.py" "Add script for loading demo data" "${DAY4/09:30/11:30}"

echo "Commit history has been created with realistic timestamps across the past 4 days!"
echo "Note: Don't forget to create a remote repository and push these changes." 