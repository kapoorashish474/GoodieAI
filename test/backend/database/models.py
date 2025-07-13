from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from .database import Base


class Story(Base):
    """Model for Hacker News stories."""
    __tablename__ = "stories"
    
    id = Column(Integer, primary_key=True, index=True)  # HN story ID
    title = Column(Text, nullable=False)
    url = Column(Text)
    time = Column(DateTime, nullable=False)
    score = Column(Integer, default=0)
    descendants = Column(Integer, default=0)  # Number of comments
    author = Column(String(255))
    fetched_at = Column(DateTime, default=func.now())


class Analytics(Base):
    """Model for keyword analytics."""
    __tablename__ = "analytics"
    
    keyword = Column(String(255), primary_key=True, index=True)
    count = Column(Integer, default=0)
    last_seen = Column(DateTime, default=func.now())


class Domain(Base):
    """Model for domain analytics."""
    __tablename__ = "domains"
    
    domain = Column(String(255), primary_key=True, index=True)
    count = Column(Integer, default=0) 