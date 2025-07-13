#!/usr/bin/env python3
"""
Pytest-compatible test file for backend functionality.
"""

import pytest
import httpx
from backend.services.hn_service import HackerNewsService
from backend.services.analytics_service import AnalyticsService


@pytest.mark.asyncio
async def test_hn_service():
    """Test Hacker News service."""
    hn_service = HackerNewsService()
    
    # Test fetching top stories
    story_ids = await hn_service.get_top_stories()
    assert len(story_ids) > 0, "Should fetch story IDs"
    
    # Test fetching story details
    if story_ids:
        story = await hn_service.get_story(story_ids[0])
        assert story is not None, "Should fetch story details"
        assert 'title' in story, "Story should have a title"


def test_analytics_service():
    """Test analytics service."""
    analytics_service = AnalyticsService()
    
    # Test keyword extraction
    test_title = "ChatGPT and Claude are revolutionizing AI development"
    keywords = analytics_service.extract_keywords(test_title)
    assert 'chatgpt' in keywords, "Should extract ChatGPT keyword"
    assert 'claude' in keywords, "Should extract Claude keyword"
    assert 'ai' in keywords, "Should extract AI keyword"
    
    # Test domain extraction
    test_url = "https://www.openai.com/blog/gpt-4"
    domain = analytics_service.extract_domain(test_url)
    assert domain == "openai.com", f"Should extract domain 'openai.com', got '{domain}'"


@pytest.mark.asyncio
async def test_api_endpoints(client):
    """Test API endpoints using test client."""
    # Test root endpoint
    response = await client.get("/")
    assert response.status_code == 200, f"Root endpoint should return 200, got {response.status_code}"
    
    # Test health endpoint
    response = await client.get("/health")
    assert response.status_code == 200, f"Health endpoint should return 200, got {response.status_code}" 