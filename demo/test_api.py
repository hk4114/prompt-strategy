#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:5001/api"

def test_api(endpoint, description):
    print(f"\n{'='*50}")
    print(f"Testing: {description}")
    print(f"URL: {BASE_URL}{endpoint}")
    print('='*50)

    try:
        response = requests.get(f"{BASE_URL}{endpoint}")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")

        if response.status_code == 200:
            data = response.json()
            print(f"Response Length: {len(json.dumps(data, indent=2))} characters")
            print(f"First 500 chars of response:")
            print(json.dumps(data, indent=2)[:500] + "...")
            return True
        else:
            print(f"Error: {response.text}")
            return False

    except Exception as e:
        print(f"Exception: {e}")
        return False

if __name__ == "__main__":
    print("Backend API Test Suite")
    print("=" * 60)

    # Test all endpoints
    endpoints = [
        ("/categories", "Categories API"),
        ("/tips", "Tips API"),
        ("/templates", "Templates API"),
        ("/templates/tags", "Template Tags API")
    ]

    results = []
    for endpoint, description in endpoints:
        success = test_api(endpoint, description)
        results.append((description, success))

    print("\n" + "="*60)
    print("SUMMARY:")
    print("="*60)
    for description, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status} - {description}")