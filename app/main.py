from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import products, sales, inventory, analytics, insights

# Simple API for e-commerce management
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="E-commerce admin dashboard API with real-time updates and insights.",
)

# Allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routes
for router in [products, sales, inventory, analytics, insights]:
    app.include_router(router.router, prefix=settings.API_V1_STR)
    # If the router has startup event handlers, register them
    if hasattr(router.router, "on_startup"):
        for handler in router.router.on_startup:
            app.add_event_handler("startup", handler)


@app.get("/")
def root():
    """Welcome page with API info."""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "features": [
            "Live Dashboard",
            "Sales Analytics",
            "Stock Management",
            "Business Insights",
        ],
    }
