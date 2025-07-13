"""
Story-related API routes.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from ...database.database import get_db
from ...database import crud
from ...schemas import StoryListResponse, Story
from ...services.hn_service import HackerNewsService
from ...services.redis_service import RedisService

router = APIRouter()

# Initialize services
hn_service = HackerNewsService()
redis_service = RedisService()


@router.post("/fetch-stories", response_model=dict)
async def fetch_stories(db: Session = Depends(get_db)):
    """Fetch and store top stories from Hacker News."""
    try:
        # Fetch stories from HN API
        hn_stories = await hn_service.get_top_stories_details()
        
        new_stories = 0
        for hn_story in hn_stories:
            story_data = hn_service.extract_story_data(hn_story)
            
            # Check if story already exists
            existing_story = crud.get_story(db, story_data['id'])
            if not existing_story:
                # Create new story
                story = crud.get_or_create_story(db, story_data)
                new_stories += 1
                
                # Publish event to Redis with serializable data
                serializable_data = {
                    'id': story_data['id'],
                    'title': story_data['title'],
                    'url': story_data['url'],
                    'time': story_data['time'].isoformat() if hasattr(story_data['time'], 'isoformat') else str(story_data['time']),
                    'score': story_data['score'],
                    'descendants': story_data['descendants'],
                    'author': story_data['author']
                }
                redis_service.publish_story_event(story.id, serializable_data)
        
        return {
            "message": f"Successfully processed {len(hn_stories)} stories",
            "new_stories": new_stories,
            "total_stories": len(hn_stories)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stories: {str(e)}")


@router.get("/stories", response_model=StoryListResponse)
async def get_stories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    keyword: Optional[str] = None,
    domain: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get stories with optional filtering."""
    stories = crud.get_stories(db, skip=skip, limit=limit, keyword=keyword, domain=domain)
    total = crud.get_stories_count(db)
    
    return StoryListResponse(
        stories=stories,
        total=total,
        page=skip // limit + 1,
        per_page=limit
    )


@router.get("/stories/{story_id}", response_model=Story)
async def get_story(story_id: int, db: Session = Depends(get_db)):
    """Get a specific story by ID."""
    story = crud.get_story(db, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story 