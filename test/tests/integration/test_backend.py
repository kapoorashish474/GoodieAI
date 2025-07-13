#!/usr/bin/env python3
"""
Simple test script to verify backend functionality.
"""

import asyncio
import httpx
import json
from backend.services.hn_service import HackerNewsService
from backend.services.analytics_service import AnalyticsService


async def test_hn_service():
    """Test Hacker News service."""
    print("Testing Hacker News Service...")
    
    hn_service = HackerNewsService()
    
    try:
        # Test fetching top stories
        story_ids = await hn_service.get_top_stories()
        print(f"✓ Fetched {len(story_ids)} story IDs")
        
        # Test fetching story details
        if story_ids:
            story = await hn_service.get_story(story_ids[0])
            print(f"✓ Fetched story details: {story.get('title', 'No title')[:50]}...")
        
        return True
    except Exception as e:
        print(f"✗ Hacker News service test failed: {e}")
        return False


def test_analytics_service():
    """Test analytics service."""
    print("Testing Analytics Service...")
    
    analytics_service = AnalyticsService()
    
    try:
        # Test keyword extraction
        test_title = "ChatGPT and Claude are revolutionizing AI development"
        keywords = analytics_service.extract_keywords(test_title)
        print(f"✓ Extracted keywords: {keywords}")
        
        # Test domain extraction
        test_url = "https://www.openai.com/blog/gpt-4"
        domain = analytics_service.extract_domain(test_url)
        print(f"✓ Extracted domain: {domain}")
        
        return True
    except Exception as e:
        print(f"✗ Analytics service test failed: {e}")
        return False


async def test_api_endpoints():
    """Test API endpoints."""
    print("Testing API Endpoints...")
    
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        try:
            # Test root endpoint
            response = await client.get(f"{base_url}/")
            if response.status_code == 200:
                print("✓ Root endpoint working")
            else:
                print(f"✗ Root endpoint failed: {response.status_code}")
                return False
            
            # Test health endpoint
            response = await client.get(f"{base_url}/health")
            if response.status_code == 200:
                print("✓ Health endpoint working")
            else:
                print(f"✗ Health endpoint failed: {response.status_code}")
                return False
            
            return True
        except Exception as e:
            print(f"✗ API test failed: {e}")
            return False


async def main():
    """Run all tests."""
    print("🧪 Running Backend Tests\n")
    
    # Test services
    hn_ok = await test_hn_service()
    analytics_ok = test_analytics_service()
    
    print("\n" + "="*50 + "\n")
    
    # Test API (only if server is running)
    print("Note: API tests require the server to be running on localhost:8000")
    api_ok = await test_api_endpoints()
    
    print("\n" + "="*50 + "\n")
    
    # Summary
    print("📊 Test Summary:")
    print(f"Hacker News Service: {'✓ PASS' if hn_ok else '✗ FAIL'}")
    print(f"Analytics Service: {'✓ PASS' if analytics_ok else '✗ FAIL'}")
    print(f"API Endpoints: {'✓ PASS' if api_ok else '✗ FAIL (server not running)'}")
    
    if hn_ok and analytics_ok:
        print("\n🎉 Core backend functionality is working!")
        print("You can now start the API server with: python main.py api")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")


if __name__ == "__main__":
    asyncio.run(main()) 