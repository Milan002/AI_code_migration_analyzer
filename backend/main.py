"""
FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database.mongodb import connect_to_mongodb, close_mongodb_connection
from app.routes.migration import router as migration_router
from app.routes.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    await connect_to_mongodb()
    yield
    # Shutdown
    await close_mongodb_connection()


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="Analyze Python codebases for Python 2 to Python 3 migration readiness",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://frontend:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(migration_router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.APP_NAME,
        "version": "1.0.0",
        "description": "Python 2 to Python 3 Migration Readiness Analyzer",
        "endpoints": {
            "analyze": "POST /api/migration/analyze",
            "get_report": "GET /api/migration/report/{report_id}",
            "list_reports": "GET /api/migration/reports"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for container orchestration."""
    return {"status": "healthy"}
