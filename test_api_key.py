#!/usr/bin/env python
"""
Test script to verify JSearch API key is working correctly
"""
import requests
import sys

def test_api_key(api_key):
    """Test if the API key is valid and has access to JSearch"""
    
    print("=" * 60)
    print("JSearch API Key Test")
    print("=" * 60)
    print(f"\nTesting API Key: {api_key[:20]}...")
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    
    params = {
        "query": "Python Developer",
        "page": "1",
        "num_pages": "1",
        "date_posted": "month",
        "country": "IN"
    }
    
    print("\nAttempting to search for Python Developer jobs...")
    print(f"URL: https://jsearch.p.rapidapi.com/search")
    print(f"Params: {params}\n")
    
    try:
        response = requests.get(
            "https://jsearch.p.rapidapi.com/search",
            headers=headers,
            params=params,
            timeout=15
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}\n")
        
        if response.status_code == 200:
            data = response.json()
            jobs = data.get('data', [])
            print("✅ SUCCESS!")
            print(f"Found {len(jobs)} jobs")
            if jobs:
                print(f"\nSample job:")
                print(f"  Title: {jobs[0].get('job_title')}")
                print(f"  Company: {jobs[0].get('employer_name')}")
            return True
            
        elif response.status_code == 403:
            print("❌ ERROR 403: Not subscribed to this API")
            print("\nPossible causes:")
            print("  1. API subscription is not active")
            print("  2. API key is invalid or expired")
            print("  3. RapidAPI is still initializing the subscription")
            print("  4. Free tier subscription doesn't include this endpoint")
            print("\nSolution:")
            print("  - Check RapidAPI dashboard to verify subscription is active")
            print("  - Ensure the API key has been reset recently")
            print("  - Wait 5-10 minutes for RapidAPI to activate the subscription")
            print("  - Consider upgrading to a paid plan if on free tier")
            return False
            
        elif response.status_code == 429:
            print("❌ ERROR 429: Too many requests")
            print("\nThis usually means rate limit exceeded")
            print("Wait a moment and try again")
            return False
            
        else:
            print(f"❌ ERROR {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception occurred: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        # Use the default from settings
        from main.job_api import DEFAULT_JSEARCH_API_KEY
        api_key = DEFAULT_JSEARCH_API_KEY
    
    success = test_api_key(api_key)
    sys.exit(0 if success else 1)
