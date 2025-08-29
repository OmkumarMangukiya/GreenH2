#!/usr/bin/env python3
"""
Test API endpoints
"""

import requests
import json

# Test status endpoint
print("Testing optimizer status...")
try:
    response = requests.get("http://localhost:8000/optimizer/status")
    if response.status_code == 200:
        status = response.json()
        print(f"✅ Status: {status.get('status')}")
        print(f"✅ Engine: {status.get('engine')}")
        print(f"✅ Database: {status.get('database_connected')}")
    else:
        print(f"❌ Status code: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test optimization endpoint
print("\nTesting optimization...")
try:
    criteria = {
        "region": "gujarat",
        "max_cost": 5.0,
        "min_production": 1000,
        "proximity_to_grid": True
    }
    response = requests.post("http://localhost:8000/api/optimize", json=criteria)
    if response.status_code == 200:
        result = response.json()
        metadata = result.get("metadata", {})
        print(f"✅ Algorithm: {metadata.get('algorithm')}")
        print(f"✅ Sites found: {metadata.get('total_sites_found')}")
        if result.get("features"):
            lcoh = result["features"][0]["properties"]["lcoh"]
            print(f"✅ Sample LCOH: ${lcoh:.2f}/kg")
    else:
        print(f"❌ Status code: {response.status_code}")
        print(f"❌ Response: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n🎉 API testing completed!")
