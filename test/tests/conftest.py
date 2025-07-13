"""
Pytest configuration and common fixtures for Hacker News Analytics Dashboard tests.
"""

import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient
from backend.api.app import app


@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def client():
    """Create a test client for the FastAPI application."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def sample_story():
    """Sample story data for testing."""
    return {
        "id": 12345,
        "title": "ChatGPT and Claude are revolutionizing AI development",
        "url": "https://www.openai.com/blog/gpt-4",
        "score": 100,
        "time": 1640995200,
        "by": "test_user",
        "descendants": 50,
        "type": "story"
    }


@pytest.fixture
def sample_analytics():
    """Sample analytics data for testing."""
    return {
        "keyword": "chatgpt",
        "frequency": 25,
        "last_updated": "2024-01-01T00:00:00Z"
    } 