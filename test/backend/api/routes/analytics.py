"""
Analytics-related API routes.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from ...database.database import get_db
from ...database import crud
from ...schemas import Analytics, Domain, DashboardResponse
from ...services.analytics_service import AnalyticsService

router = APIRouter()

# Initialize services
analytics_service = AnalyticsService()


@router.get("/analytics", response_model=List[Analytics])
async def get_analytics(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get top analytics by frequency."""
    return crud.get_analytics(db, limit=limit)


@router.get("/domains", response_model=List[Domain])
async def get_domains(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get top domains by frequency."""
    return crud.get_domains(db, limit=limit)


@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(db: Session = Depends(get_db)):
    """Get dashboard data including stories, analytics, and domains."""
    # Get recent stories
    stories = crud.get_stories(db, skip=0, limit=10)
    
    # Get top analytics
    analytics = crud.get_analytics(db, limit=10)
    
    # Get top domains
    domains = crud.get_domains(db, limit=10)
    
    # Get counts
    total_stories = crud.get_stories_count(db)
    total_keywords = crud.get_analytics_count(db)
    total_domains = crud.get_domains_count(db)
    
    return DashboardResponse(
        stories=stories,
        analytics=analytics,
        domains=domains,
        total_stories=total_stories,
        total_keywords=total_keywords,
        total_domains=total_domains
    )


@router.post("/process-story/{story_id}")
async def process_story(story_id: int, db: Session = Depends(get_db)):
    """Manually process a story for analytics."""
    story = crud.get_story(db, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    result = analytics_service.process_story(db, story)
    
    return {
        "message": "Story processed successfully",
        "story_id": story_id,
        "keywords_found": result['keywords'],
        "domain": result['domain']
    } 