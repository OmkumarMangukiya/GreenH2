#!/usr/bin/env python3
"""
Test script to check optimizer status
"""

from optimizer import get_optimization_status

if __name__ == "__main__":
    status = get_optimization_status()
    print("Optimizer Status:")
    print(f"Status: {status.get('status')}")
    print(f"Engine: {status.get('engine')}")
    print(f"Database Connected: {status.get('database_connected')}")
    print(f"Capabilities: {len(status.get('capabilities', []))} features")
    print(f"Supported Regions: {status.get('supported_regions', [])}")
