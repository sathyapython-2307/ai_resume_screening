#!/usr/bin/env python
"""
Comprehensive RapidAPI Subscription Diagnostic Tool
Checks subscription status and provides detailed troubleshooting info
"""
import requests
import json
from datetime import datetime

def check_rapidapi_subscription():
    """Check RapidAPI subscription status and provide diagnostics"""
    
    api_key = "ak_0kd18786e2nzusm60nw0adtx8q5rtxbrjmph67vvf5zttv2"
    
    print("=" * 80)
    print("RAPIDAPI SUBSCRIPTION DIAGNOSTIC TOOL")
    print("=" * 80)
    print(f"\nDiagnostic Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API Key: {api_key[:20]}{'*' * (len(api_key) - 20)}")
    
    # Test 1: Check API connectivity
    print("\n" + "=" * 80)
    print("TEST 1: Basic API Connectivity")
    print("=" * 80)
    
    try:
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }
        
        response = requests.get(
            "https://jsearch.p.rapidapi.com/search",
            headers=headers,
            params={
                "query": "test",
                "page": "1",
                "num_pages": "1"
            },
            timeout=10
        )
        
        print(f"✓ Connection: SUCCESS")
        print(f"✓ Status Code: {response.status_code}")
        print(f"✓ Response Time: {response.elapsed.total_seconds():.2f}s")
        
    except Exception as e:
        print(f"✗ Connection: FAILED")
        print(f"✗ Error: {e}")
        return
    
    # Test 2: Analyze Response Headers
    print("\n" + "=" * 80)
    print("TEST 2: Response Headers Analysis")
    print("=" * 80)
    
    important_headers = {
        'X-RapidAPI-Version': 'API Version',
        'X-RapidAPI-Region': 'Region',
        'X-RapidAPI-Request-Id': 'Request ID',
        'Content-Type': 'Response Type',
    }
    
    for header, label in important_headers.items():
        value = response.headers.get(header, 'N/A')
        print(f"  {label}: {value}")
    
    # Test 3: Analyze Error Response
    print("\n" + "=" * 80)
    print("TEST 3: Error Response Analysis")
    print("=" * 80)
    
    try:
        error_data = response.json()
        print(f"✓ Response is valid JSON")
        print(f"✓ Error Message: {error_data.get('message', 'N/A')}")
        
        if 'data' in error_data:
            print(f"✓ Contains data field")
        
    except:
        print(f"✗ Response is not valid JSON")
    
    # Test 4: Common Issues Diagnosis
    print("\n" + "=" * 80)
    print("TEST 4: Issue Diagnosis")
    print("=" * 80)
    
    if response.status_code == 403:
        print("\n❌ STATUS: 403 Forbidden - Not Subscribed")
        print("\nPossible Causes:")
        print("  1. ⚠️  Subscription is NOT active yet")
        print("  2. ⚠️  API key is invalid or expired")
        print("  3. ⚠️  RapidAPI is initializing subscription (wait 5-10 min)")
        print("  4. ⚠️  Free tier subscription expired")
        print("  5. ⚠️  API key doesn't match current subscription")
        
        print("\n✅ Solutions to Try (in order):")
        print("  Step 1: Go to https://rapidapi.com/dashboard")
        print("  Step 2: Click on 'My Subscriptions'")
        print("  Step 3: Look for 'JSearch' API")
        print("  Step 4: Verify status is 'Active' (not Pending/Expired/Cancelled)")
        print("  Step 5: If status is wrong, click on the subscription")
        print("  Step 6: Go to 'API Keys' tab")
        print("  Step 7: Copy the default key")
        print("  Step 8: Paste it in main/job_api.py (line 13)")
        print("  Step 9: Wait 5-10 minutes for RapidAPI to activate")
        print("  Step 10: Run this test again")
        
    elif response.status_code == 429:
        print("\n⚠️  STATUS: 429 Too Many Requests")
        print("\nThis means:")
        print("  - Rate limit has been exceeded")
        print("  - Your subscription might be on free tier (very limited)")
        print("\nSolution:")
        print("  - Wait a few minutes before retrying")
        print("  - Consider upgrading to a paid plan for higher limits")
    
    elif response.status_code == 200:
        print("\n✅ STATUS: 200 OK - API is Working!")
        data = response.json()
        jobs = data.get('data', [])
        print(f"\n✅ Subscription is ACTIVE and WORKING")
        print(f"✅ Found {len(jobs)} jobs in response")
        if jobs:
            print(f"✅ Sample job: {jobs[0].get('job_title', 'N/A')}")
    
    else:
        print(f"\n⚠️  STATUS: {response.status_code} - Unexpected Response")
        print(f"Response: {response.text[:200]}")
    
    # Test 5: RapidAPI Account Info
    print("\n" + "=" * 80)
    print("TEST 5: RapidAPI Account Check (Manual Steps Required)")
    print("=" * 80)
    print("\nTo verify your subscription manually:")
    print("  1. Go to https://rapidapi.com/dashboard")
    print("  2. In left sidebar, click 'My Subscriptions'")
    print("  3. Look for 'JSearch - Job Search API'")
    print("  4. Verify the subscription shows:")
    print("       ✓ Status: Active")
    print("       ✓ Plan: Free (or paid)")
    print("       ✓ Remaining Requests: > 0")
    print("  5. Click on the subscription to view details")
    print("  6. Go to 'API Keys' tab")
    print("  7. Copy the 'X-RapidAPI-Key'")
    print("\nIf subscription is MISSING:")
    print("  1. Go to https://rapidapi.com/api-rapid/api/jsearch")
    print("  2. Click 'Subscribe to Test'")
    print("  3. Select a plan (Free is available)")
    print("  4. Click 'Subscribe'")
    print("  5. Wait 5-10 minutes for activation")
    print("  6. Get the new API key from dashboard")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    if response.status_code == 200:
        print("✅ Your API is fully functional!")
        print("✅ Job search should work now")
    else:
        print(f"❌ Your API has status code {response.status_code}")
        print("❌ Follow the solutions above to fix it")
    
    print("\n" + "=" * 80)
    print("Need help? Keep this output for reference")
    print("=" * 80)

if __name__ == "__main__":
    check_rapidapi_subscription()
