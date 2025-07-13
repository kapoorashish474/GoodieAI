"""
Story-related background tasks.
"""

from celery import current_task
from sqlalchemy.orm import Session
from ..core.celery_app import celery_app
from ..database.database import SessionLocal
from ..services.hn_service import HackerNewsService
from ..services.analytics_service import AnalyticsService
from ..database import crud
import asyncio


@celery_app.task(bind=True)
def fetch_and_process_stories(self):
    """Fetch top stories from HN and process them for analytics."""
    try:
        # Update task state
        self.update_state(state="PROGRESS", meta={"status": "Fetching stories from HN API"})
        
        # Create services
        hn_service = HackerNewsService()
        analytics_service = AnalyticsService()
        
        # Get database session
        db = SessionLocal()
        
        try:
            # Fetch top stories
            story_ids = asyncio.run(hn_service.get_top_stories())
            self.update_state(state="PROGRESS", meta={"status": f"Fetched {len(story_ids)} story IDs"})
            
            processed_count = 0
            for i, story_id in enumerate(story_ids):
                try:
                    # Check if story already exists
                    existing_story = crud.get_story(db, story_id)
                    if existing_story:
                        continue
                    
                    # Fetch story details
                    story_data = asyncio.run(hn_service.get_story(story_id))
                    
                    if not story_data or story_data.get('type') != 'story':
                        continue
                    
                    # Debug: Print story data structure
                    print(f"Processing story {story_id}: {story_data.get('title', 'No title')}")
                    print(f"Story data keys: {list(story_data.keys())}")
                    
                    # Create story in database
                    story = crud.create_story_from_dict(db, story_data)
                    
                    # Process for analytics
                    analytics_service.process_story(db, story)
                    
                    processed_count += 1
                    
                    # Update progress
                    progress = int((i + 1) / len(story_ids) * 100)
                    self.update_state(
                        state="PROGRESS", 
                        meta={
                            "status": f"Processed {processed_count} new stories",
                            "progress": progress
                        }
                    )
                    
                except Exception as e:
                    print(f"Error processing story {story_id}: {e}")
                    continue
            
            return {
                "status": "SUCCESS",
                "processed_count": processed_count,
                "total_stories": len(story_ids)
            }
            
        finally:
            db.close()
            
    except Exception as e:
        self.update_state(state="FAILURE", meta={"error": str(e)})
        raise


@celery_app.task
def process_story_analytics(story_id: int, story_data: dict):
    """Process a single story for analytics."""
    try:
        analytics_service = AnalyticsService()
        db = SessionLocal()
        
        try:
            # Create story if it doesn't exist
            existing_story = crud.get_story(db, story_id)
            if not existing_story:
                story = crud.create_story_from_dict(db, story_data)
            else:
                story = existing_story
            
            # Process analytics
            analytics_service.process_story(db, story)
            
            return {"status": "SUCCESS", "story_id": story_id}
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"Error processing analytics for story {story_id}: {e}")
        return {"status": "FAILURE", "error": str(e), "story_id": story_id}


@celery_app.task
def update_analytics_summary():
    """Update analytics summary tables."""
    try:
        db = SessionLocal()
        
        try:
            # This could include aggregating data, cleaning old records, etc.
            # For now, just return success
            return {"status": "SUCCESS", "message": "Analytics summary updated"}
            
        finally:
            db.close()
            
    except Exception as e:
        return {"status": "FAILURE", "error": str(e)} 