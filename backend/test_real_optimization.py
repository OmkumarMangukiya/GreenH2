#!/usr/bin/env python3
"""
Test real optimization
"""

from optimizer import run_optimization
import json

criteria = {
    'region': 'gujarat',
    'max_cost': 5.0,
    'min_production': 1000,
    'proximity_to_grid': True
}

print('Testing optimization with real data...')
result = run_optimization(criteria)
print(f'Algorithm used: {result.get("metadata", {}).get("algorithm", "Unknown")}')
print(f'Total sites found: {result.get("metadata", {}).get("total_sites_found", 0)}')
if result.get('features'):
    print(f'First site LCOH: ${result["features"][0]["properties"]["lcoh"]:.2f}/kg')
print('✅ Optimization completed successfully!')
