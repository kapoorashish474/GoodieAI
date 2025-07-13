"""
Response-related Pydantic schemas.
"""

from pydantic import BaseModel
from typing import List
from .story import Story
from .analytics import Analytics, Domain


class DashboardResponse(BaseModel):
    """Schema for dashboard response."""
    stories: List[Story]
    analytics: List[Analytics]
    domains: List[Domain]
    total_stories: int
    total_keywords: int
    total_domains: int 