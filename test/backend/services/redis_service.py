import redis
import json
from typing import Optional, Callable
from ..core.config import settings
from datetime import datetime


class RedisService:
    """Service for Redis pub/sub operations."""
    
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL)
        self.pubsub = self.redis_client.pubsub()
    
    def publish_story_event(self, story_id: int, story_data: dict):
        """Publish a new story event to Redis."""
        event_data = {
            'story_id': story_id,
            'story_data': story_data,
            'timestamp': str(datetime.now())
        }
        self.redis_client.publish('new_story', json.dumps(event_data))
    
    def subscribe_to_stories(self, callback: Callable[[dict], None]):
        """Subscribe to new story events."""
        self.pubsub.subscribe('new_story')
        
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                try:
                    data = json.loads(message['data'])
                    callback(data)
                except json.JSONDecodeError:
                    print(f"Failed to decode message: {message['data']}")
    
    def get_story_event(self) -> Optional[dict]:
        """Get a single story event (non-blocking)."""
        message = self.pubsub.get_message()
        if message and message['type'] == 'message':
            try:
                return json.loads(message['data'])
            except json.JSONDecodeError:
                return None
        return None
    
    def close(self):
        """Close Redis connections."""
        self.pubsub.close()
        self.redis_client.close() 