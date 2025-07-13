"""
FastAPI application factory.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ..core.config import settings
from ..database.models import Base
from ..database.database import engine
from .routes import stories, analytics, tasks

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Real-Time Hacker News Analytics Dashboard API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(stories.router, prefix="/api/v1", tags=["stories"])
app.include_router(analytics.router, prefix="/api/v1", tags=["analytics"])
app.include_router(tasks.router, prefix="/api/v1", tags=["tasks"])


@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Hacker News Analytics Dashboard API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"} 