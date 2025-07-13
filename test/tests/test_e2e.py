#!/usr/bin/env python3
"""
End-to-End Test Script for Hacker News Analytics Dashboard
"""

import requests
import time
import json
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def test_backend_health():
    """Test backend health endpoint."""
    print("🔍 Testing Backend Health...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Backend is healthy")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend health check error: {e}")
        return False

def test_frontend_access():
    """Test frontend accessibility."""
    print("🔍 Testing Frontend Access...")
    try:
        response = requests.get(FRONTEND_URL)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            return True
        else:
            print(f"❌ Frontend access failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend access error: {e}")
        return False

def test_dashboard_api():
    """Test dashboard API endpoint."""
    print("🔍 Testing Dashboard API...")
    try:
        response = requests.get(f"{API_BASE_URL}/dashboard")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Dashboard API working - Stories: {data['total_stories']}, Keywords: {data['total_keywords']}")
            return True
        else:
            print(f"❌ Dashboard API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Dashboard API error: {e}")
        return False

def test_story_fetching():
    """Test story fetching functionality."""
    print("🔍 Testing Story Fetching...")
    try:
        # Trigger story fetching
        response = requests.post(f"{API_BASE_URL}/tasks/fetch-stories/")
        if response.status_code == 200:
            task_data = response.json()
            task_id = task_data['task_id']
            print(f"✅ Story fetching task started: {task_id}")
            
            # Wait and check task status
            for i in range(10):  # Wait up to 30 seconds
                time.sleep(3)
                status_response = requests.get(f"{API_BASE_URL}/tasks/{task_id}")
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    print(f"   Task status: {status_data['state']} - {status_data.get('status', '')}")
                    
                    if status_data['state'] == 'SUCCESS':
                        print("✅ Story fetching completed successfully")
                        return True
                    elif status_data['state'] == 'FAILURE':
                        print(f"❌ Story fetching failed: {status_data.get('status', '')}")
                        return False
            
            print("⚠️ Story fetching task still running (timeout)")
            return False
        else:
            print(f"❌ Story fetching request failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Story fetching error: {e}")
        return False

def test_analytics_data():
    """Test analytics data after story fetching."""
    print("🔍 Testing Analytics Data...")
    try:
        # Wait a bit for processing
        time.sleep(5)
        
        # Check analytics
        analytics_response = requests.get(f"{API_BASE_URL}/analytics")
        if analytics_response.status_code == 200:
            analytics = analytics_response.json()
            print(f"✅ Analytics API working - Found {len(analytics)} keywords")
            
            # Check domains
            domains_response = requests.get(f"{API_BASE_URL}/domains")
            if domains_response.status_code == 200:
                domains = domains_response.json()
                print(f"✅ Domains API working - Found {len(domains)} domains")
                
                # Check stories
                stories_response = requests.get(f"{API_BASE_URL}/stories?limit=5")
                if stories_response.status_code == 200:
                    stories_data = stories_response.json()
                    print(f"✅ Stories API working - Total stories: {stories_data['total']}")
                    
                    if stories_data['total'] > 0:
                        print("✅ Data pipeline is working - Stories are being processed")
                        return True
                    else:
                        print("⚠️ No stories found - may need to wait longer")
                        return False
                else:
                    print(f"❌ Stories API failed: {stories_response.status_code}")
                    return False
            else:
                print(f"❌ Domains API failed: {domains_response.status_code}")
                return False
        else:
            print(f"❌ Analytics API failed: {analytics_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Analytics data error: {e}")
        return False

def test_frontend_dashboard():
    """Test frontend dashboard page."""
    print("🔍 Testing Frontend Dashboard...")
    try:
        response = requests.get(f"{FRONTEND_URL}/dashboard")
        if response.status_code == 200:
            if "Hacker News Analytics Dashboard" in response.text:
                print("✅ Frontend dashboard is loading correctly")
                return True
            else:
                print("❌ Frontend dashboard content not found")
                return False
        else:
            print(f"❌ Frontend dashboard failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend dashboard error: {e}")
        return False

def test_frontend_explorer():
    """Test frontend explorer page."""
    print("🔍 Testing Frontend Explorer...")
    try:
        response = requests.get(f"{FRONTEND_URL}/explorer")
        if response.status_code == 200:
            if "Story Explorer" in response.text:
                print("✅ Frontend explorer is loading correctly")
                return True
            else:
                print("❌ Frontend explorer content not found")
                return False
        else:
            print(f"❌ Frontend explorer failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend explorer error: {e}")
        return False

def main():
    """Run all end-to-end tests."""
    print("🚀 Starting End-to-End Tests")
    print("=" * 50)
    print(f"Timestamp: {datetime.now()}")
    print()
    
    tests = [
        ("Backend Health", test_backend_health),
        ("Frontend Access", test_frontend_access),
        ("Dashboard API", test_dashboard_api),
        ("Story Fetching", test_story_fetching),
        ("Analytics Data", test_analytics_data),
        ("Frontend Dashboard", test_frontend_dashboard),
        ("Frontend Explorer", test_frontend_explorer),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        print("-" * 30)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is working correctly.")
        print("\n🌐 You can now access:")
        print(f"   Frontend: {FRONTEND_URL}")
        print(f"   Backend API Docs: {API_BASE_URL}/docs")
    else:
        print("⚠️ Some tests failed. Check the logs above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 