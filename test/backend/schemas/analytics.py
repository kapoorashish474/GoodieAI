"""
Analytics-related Pydantic schemas.
"""

from pydantic import BaseModel
from datetime import datetime


class AnalyticsBase(BaseModel):
    """Base analytics schema."""
    keyword: str
    count: int
    last_seen: datetime


class Analytics(AnalyticsBase):
    """Schema for analytics response."""
    
    class Config:
        from_attributes = True


class DomainBase(BaseModel):
    """Base domain schema."""
    domain: str
    count: int


class Domain(DomainBase):
    """Schema for domain response."""
    
    class Config:
        from_attributes = True 