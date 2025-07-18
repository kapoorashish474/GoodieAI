from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from . import models
from .. import schemas


def get_story(db: Session, story_id: int) -> Optional[models.Story]:
    """Get a story by ID."""
    return db.query(models.Story).filter(models.Story.id == story_id).first()


def get_stories(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    keyword: Optional[str] = None,
    domain: Optional[str] = None
) -> List[models.Story]:
    """Get stories with optional filtering."""
    query = db.query(models.Story)
    
    if keyword:
        query = query.filter(models.Story.title.ilike(f"%{keyword}%"))
    
    if domain:
        query = query.filter(models.Story.url.ilike(f"%{domain}%"))
    
    return query.order_by(desc(models.Story.score)).offset(skip).limit(limit).all()


def create_story(db: Session, story: schemas.StoryCreate) -> models.Story:
    """Create a new story."""
    db_story = models.Story(**story.dict())
    db.add(db_story)
    db.commit()
    db.refresh(db_story)
    return db_story


def create_story_from_dict(db: Session, story_data: dict) -> models.Story:
    """Create a new story from raw dictionary data."""
    # Convert timestamp to datetime if needed
    if 'time' in story_data and isinstance(story_data['time'], (int, float)):
        from datetime import datetime
        story_data['time'] = datetime.fromtimestamp(story_data['time'])
    
    # Map HN API fields to model fields
    story_dict = {
        'id': story_data.get('id'),
        'title': story_data.get('title', ''),
        'url': story_data.get('url'),
        'time': story_data.get('time'),
        'score': story_data.get('score', 0),
        'descendants': story_data.get('descendants', 0),
        'author': story_data.get('by')  # HN API uses 'by' for author
    }
    
    db_story = models.Story(**story_dict)
    db.add(db_story)
    db.commit()
    db.refresh(db_story)
    return db_story


def get_or_create_story(db: Session, story_data: dict) -> models.Story:
    """Get existing story or create new one."""
    story_id = story_data['id']
    existing_story = get_story(db, story_id)
    
    if existing_story:
        return existing_story
    
    # Debug: Print incoming data
    print(f"Creating story {story_id} with data: {story_data}")
    
    # Use the helper function to create story from dict
    return create_story_from_dict(db, story_data)


def get_analytics(db: Session, limit: int = 10) -> List[models.Analytics]:
    """Get top analytics by frequency."""
    return db.query(models.Analytics).order_by(desc(models.Analytics.count)).limit(limit).all()


def get_domains(db: Session, limit: int = 10) -> List[models.Domain]:
    """Get top domains by frequency."""
    return db.query(models.Domain).order_by(desc(models.Domain.count)).limit(limit).all()


def get_stories_count(db: Session) -> int:
    """Get total number of stories."""
    return db.query(models.Story).count()


def get_analytics_count(db: Session) -> int:
    """Get total number of analytics entries."""
    return db.query(models.Analytics).count()


def get_domains_count(db: Session) -> int:
    """Get total number of domains."""
    return db.query(models.Domain).count() 


def create_ai_keyword(db: Session, keyword: str, status: str = "active") -> models.AIKeyword:
    """Create a new AI keyword entry."""
    ai_keyword = models.AIKeyword(keyword=keyword, status=status)
    db.add(ai_keyword)
    db.commit()
    db.refresh(ai_keyword)
    return ai_keyword

def get_ai_keywords(db: Session):
    """Get all AI keywords."""
    return db.query(models.AIKeyword).all() 