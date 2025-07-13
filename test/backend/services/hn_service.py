import httpx
import asyncio
from typing import List, Dict, Any
from datetime import datetime
from ..core.config import settings


class HackerNewsService:
    """Service for fetching data from Hacker News API."""
    
    def __init__(self):
        self.base_url = settings.HN_API_BASE_URL
        self.limit = settings.HN_TOP_STORIES_LIMIT
    
    async def get_top_stories(self) -> List[int]:
        """Fetch top story IDs from HN API."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/topstories.json")
            response.raise_for_status()
            story_ids = response.json()
            return story_ids[:self.limit]
    
    async def get_story(self, story_id: int) -> Dict[str, Any]:
        """Fetch individual story details from HN API."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/item/{story_id}.json")
            response.raise_for_status()
            return response.json()
    
    async def get_top_stories_details(self) -> List[Dict[str, Any]]:
        """Fetch details for top stories."""
        story_ids = await self.get_top_stories()
        
        # Fetch story details concurrently
        tasks = [self.get_story(story_id) for story_id in story_ids]
        stories = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out failed requests and non-story items
        valid_stories = []
        for story in stories:
            if isinstance(story, dict) and story.get('type') == 'story':
                # Convert timestamp to datetime
                if 'time' in story:
                    story['time'] = datetime.fromtimestamp(story['time'])
                valid_stories.append(story)
        
        return valid_stories
    
    def extract_story_data(self, hn_story: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant fields from HN story data."""
        return {
            'id': hn_story.get('id'),
            'title': hn_story.get('title', ''),
            'url': hn_story.get('url'),
            'time': hn_story.get('time'),
            'score': hn_story.get('score', 0),
            'descendants': hn_story.get('descendants', 0),
            'author': hn_story.get('by')
        } 