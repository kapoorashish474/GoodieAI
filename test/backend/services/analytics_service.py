import re
from typing import List, Dict, Set
from urllib.parse import urlparse
from sqlalchemy.orm import Session
from ..database.models import Story, Analytics, Domain
from ..core.config import settings


class AnalyticsService:
    """Service for processing stories and generating analytics."""
    
    def __init__(self):
        self.ai_keywords = set(keyword.lower() for keyword in settings.AI_KEYWORDS)
    
    def extract_keywords(self, title: str) -> Set[str]:
        """Extract AI-related keywords from story title."""
        title_lower = title.lower()
        found_keywords = set()
        
        for keyword in self.ai_keywords:
            if keyword in title_lower:
                found_keywords.add(keyword)
        
        return found_keywords
    
    def extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        if not url:
            return "unknown"
        
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            # Remove www. prefix if present
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain
        except:
            return "unknown"
    
    def process_story(self, db: Session, story: Story) -> Dict[str, List[str]]:
        """Process a story and update analytics."""
        # Extract keywords from title
        keywords = self.extract_keywords(story.title)
        
        # Extract domain from URL
        domain = self.extract_domain(story.url)
        
        # Update keyword analytics
        for keyword in keywords:
            self._update_keyword_analytics(db, keyword)
        
        # Update domain analytics
        if domain != "unknown":
            self._update_domain_analytics(db, domain)
        
        return {
            'keywords': list(keywords),
            'domain': domain
        }
    
    def _update_keyword_analytics(self, db: Session, keyword: str):
        """Update keyword frequency in analytics table."""
        from datetime import datetime
        
        analytics = db.query(Analytics).filter(Analytics.keyword == keyword).first()
        
        if analytics:
            analytics.count += 1
            analytics.last_seen = datetime.now()
        else:
            analytics = Analytics(
                keyword=keyword,
                count=1,
                last_seen=datetime.now()
            )
            db.add(analytics)
        
        db.commit()
    
    def _update_domain_analytics(self, db: Session, domain: str):
        """Update domain frequency in domains table."""
        domain_record = db.query(Domain).filter(Domain.domain == domain).first()
        
        if domain_record:
            domain_record.count += 1
        else:
            domain_record = Domain(domain=domain, count=1)
            db.add(domain_record)
        
        db.commit()
    
    def get_top_keywords(self, db: Session, limit: int = 10) -> List[Analytics]:
        """Get top keywords by frequency."""
        return db.query(Analytics).order_by(Analytics.count.desc()).limit(limit).all()
    
    def get_top_domains(self, db: Session, limit: int = 10) -> List[Domain]:
        """Get top domains by frequency."""
        return db.query(Domain).order_by(Domain.count.desc()).limit(limit).all()
    
    def get_analytics_summary(self, db: Session) -> Dict[str, int]:
        """Get analytics summary."""
        total_keywords = db.query(Analytics).count()
        total_domains = db.query(Domain).count()
        total_stories = db.query(Story).count()
        
        return {
            'total_keywords': total_keywords,
            'total_domains': total_domains,
            'total_stories': total_stories
        } 