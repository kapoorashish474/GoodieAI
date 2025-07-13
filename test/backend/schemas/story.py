"""
Story-related Pydantic schemas.
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class StoryBase(BaseModel):
    """Base story schema."""
    title: str
    url: Optional[str] = None
    time: datetime
    score: int = 0
    descendants: int = 0
    author: Optional[str] = None


class StoryCreate(StoryBase):
    """Schema for creating a story."""
    id: int  # HN story ID


class Story(StoryBase):
    """Schema for story response."""
    id: int
    fetched_at: datetime
    
    class Config:
        from_attributes = True


class StoryListResponse(BaseModel):
    """Schema for story list response."""
    stories: List[Story]
    total: int
    page: int
    per_page: int 