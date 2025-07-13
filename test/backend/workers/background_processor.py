"""
Background processor for handling Redis events.
"""

import json
import time
from sqlalchemy.orm import Session
from ..database.database import SessionLocal
from ..services.redis_service import RedisService
from ..services.analytics_service import AnalyticsService
from ..database import crud


class BackgroundProcessor:
    """Background service for processing stories from Redis events."""
    
    def __init__(self):
        self.redis_service = RedisService()
        self.analytics_service = AnalyticsService()
    
    def process_story_event(self, event_data: dict):
        """Process a story event from Redis."""
        try:
            story_id = event_data.get('story_id')
            story_data = event_data.get('story_data')
            
            if not story_id or not story_data:
                print(f"Invalid event data: {event_data}")
                return
            
            # Get database session
            db = SessionLocal()
            try:
                # Get the story from database
                story = crud.get_story(db, story_id)
                if not story:
                    print(f"Story {story_id} not found in database")
                    return
                
                # Process story for analytics
                result = self.analytics_service.process_story(db, story)
                
                print(f"Processed story {story_id}: {result['keywords']} keywords, domain: {result['domain']}")
                
            finally:
                db.close()
                
        except Exception as e:
            print(f"Error processing story event: {e}")
    
    def run(self):
        """Run the background processor."""
        print("Starting background processor...")
        print("Subscribing to Redis events...")
        
        try:
            # Subscribe to story events
            self.redis_service.subscribe_to_stories(self.process_story_event)
        except KeyboardInterrupt:
            print("Shutting down background processor...")
        finally:
            self.redis_service.close()
    
    def run_once(self):
        """Process a single event (for testing)."""
        event = self.redis_service.get_story_event()
        if event:
            self.process_story_event(event)
            return True
        return False


if __name__ == "__main__":
    processor = BackgroundProcessor()
    processor.run() 