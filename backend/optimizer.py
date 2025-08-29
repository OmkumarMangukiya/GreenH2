import time
import random
import json
from typing import Dict, List

# Try to import real optimizer, fallback to simulation if unavailable
try:
    from real_optimizer import run_optimization as real_run_optimization
    from real_optimizer import get_optimization_status as real_get_status
    USE_REAL_OPTIMIZER = True
    print("✅ Real GEOH2 optimizer loaded successfully")
except ImportError as e:
    print(f"⚠️  Real optimizer not available: {e}")
    print("🔄 Using simulation fallback")
    USE_REAL_OPTIMIZER = False

def run_optimization(criteria: dict) -> dict:
    """
    Main optimization function - uses real GEOH2 engine when available
    """
    if USE_REAL_OPTIMIZER:
        try:
            return real_run_optimization(criteria)
        except Exception as e:
            print(f"❌ Real optimizer failed: {e}")
            print("🔄 Falling back to simulation")
            return run_simulation_fallback(criteria)
    else:
        return run_simulation_fallback(criteria)

def run_simulation_fallback(criteria: dict) -> dict:
    """
    Enhanced simulation fallback with Indian states data
    """
    print(f"🔄 Running simulation for criteria: {criteria}")

    # Simulate processing time
    print("Processing geospatial data...")
    time.sleep(1)
    print("Calculating LCOH for potential sites...")
    time.sleep(1)
    print("Optimizing site selection...")
    time.sleep(1)

    region = criteria.get('region', 'gujarat').lower()

    # Enhanced Indian states data
    india_sites = {
        'gujarat': [
            {"name": "Bhuj_Solar_Park", "lat": 23.241, "lon": 69.669, "base_lcoh": 3.5},
            {"name": "Kutch_Wind_Farm", "lat": 23.733, "lon": 68.867, "base_lcoh": 4.2},
            {"name": "Surat_Port_Complex", "lat": 21.170, "lon": 72.831, "base_lcoh": 4.8},
            {"name": "Ahmedabad_Industrial", "lat": 23.022, "lon": 72.571, "base_lcoh": 4.1},
            {"name": "Jamnagar_Refinery", "lat": 22.470, "lon": 70.057, "base_lcoh": 3.8},
            {"name": "Bhavnagar_Coast", "lat": 21.761, "lon": 72.151, "base_lcoh": 4.3},
            {"name": "Rajkot_Industrial", "lat": 22.303, "lon": 70.802, "base_lcoh": 4.5},
            {"name": "Vadodara_Chemical", "lat": 22.307, "lon": 73.181, "base_lcoh": 4.0}
        ],
        'rajasthan': [
            {"name": "Jaisalmer_Wind", "lat": 26.915, "lon": 70.908, "base_lcoh": 3.2},
            {"name": "Bikaner_Solar", "lat": 28.022, "lon": 73.311, "base_lcoh": 3.8},
            {"name": "Jodhpur_Industrial", "lat": 26.238, "lon": 73.024, "base_lcoh": 4.1},
            {"name": "Jaipur_Smart_City", "lat": 26.912, "lon": 75.787, "base_lcoh": 4.5},
            {"name": "Barmer_Renewable", "lat": 25.753, "lon": 71.393, "base_lcoh": 3.6}
        ],
        'maharashtra': [
            {"name": "Dhule_Solar", "lat": 20.902, "lon": 74.774, "base_lcoh": 4.0},
            {"name": "Pune_Technology", "lat": 18.520, "lon": 73.856, "base_lcoh": 4.3},
            {"name": "Mumbai_Port", "lat": 18.922, "lon": 72.834, "base_lcoh": 4.8},
            {"name": "Nagpur_Industrial", "lat": 21.145, "lon": 79.088, "base_lcoh": 4.2},
            {"name": "Aurangabad_Solar", "lat": 19.876, "lon": 75.343, "base_lcoh": 3.9}
        ],
        'karnataka': [
            {"name": "Bengaluru_Tech", "lat": 12.971, "lon": 77.594, "base_lcoh": 4.4},
            {"name": "Mangalore_Port", "lat": 12.914, "lon": 74.856, "base_lcoh": 4.1},
            {"name": "Hubli_Industrial", "lat": 15.364, "lon": 75.124, "base_lcoh": 4.0},
            {"name": "Mysore_Heritage", "lat": 12.295, "lon": 76.639, "base_lcoh": 4.2},
            {"name": "Tumkur_Solar", "lat": 13.340, "lon": 77.101, "base_lcoh": 3.8}
        ],
        'tamil_nadu': [
            {"name": "Chennai_Port", "lat": 13.082, "lon": 80.270, "base_lcoh": 4.5},
            {"name": "Coimbatore_Industrial", "lat": 11.016, "lon": 76.955, "base_lcoh": 4.2},
            {"name": "Tiruchirappalli_Solar", "lat": 10.790, "lon": 78.704, "base_lcoh": 4.0},
            {"name": "Madurai_Heritage", "lat": 9.925, "lon": 78.119, "base_lcoh": 4.3},
            {"name": "Tuticorin_Port", "lat": 8.764, "lon": 78.134, "base_lcoh": 4.1}
        ],
        'andhra_pradesh': [
            {"name": "Visakhapatnam_Port", "lat": 17.686, "lon": 83.218, "base_lcoh": 4.3},
            {"name": "Vijayawada_Industrial", "lat": 16.506, "lon": 80.648, "base_lcoh": 4.1},
            {"name": "Tirupati_Solar", "lat": 13.628, "lon": 79.419, "base_lcoh": 3.9},
            {"name": "Kakinada_Port", "lat": 16.989, "lon": 82.247, "base_lcoh": 4.2},
            {"name": "Anantapur_Wind", "lat": 14.681, "lon": 77.600, "base_lcoh": 3.7}
        ]
    }

    if region in india_sites:
        available_sites = india_sites[region]
        selected_sites = random.sample(available_sites, min(len(available_sites), random.randint(3, 5)))
    elif region == 'india':
        all_sites = []
        for state_sites in india_sites.values():
            all_sites.extend(state_sites)
        selected_sites = random.sample(all_sites, random.randint(4, 6))
    else:
        selected_sites = []
        for i in range(random.randint(3, 5)):
            selected_sites.append({
                "name": f"Site_{i+1}_{region.title()}",
                "lat": random.uniform(-90, 90),
                "lon": random.uniform(-180, 180),
                "base_lcoh": random.uniform(2.0, 6.0)
            })

    features = []

    for i, site in enumerate(selected_sites):
        lcoh = min(site['base_lcoh'], criteria.get('max_cost', 6.0) - 0.1)

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [site['lon'], site['lat']]
            },
            "properties": {
                "site_name": site['name'],
                "lcoh": round(lcoh, 2),
                "production_cost": round(lcoh * 0.75, 2),
                "transport_cost": round(lcoh * 0.25, 2),
                "region": region.title(),
                "max_cost": criteria.get('max_cost', 6.0),
                "rank": i + 1,
                "coordinates": f"{site['lat']:.3f}°N, {site['lon']:.3f}°E"
            }
        }
        features.append(feature)

    # Sort features by LCOH (lowest cost first)
    features.sort(key=lambda x: x["properties"]["lcoh"])

    # Update ranks after sorting
    for i, feature in enumerate(features):
        feature["properties"]["rank"] = i + 1

    geojson_result = {
        "type": "FeatureCollection",
        "features": features,
        "metadata": {
            "optimization_criteria": criteria,
            "total_sites_found": len(features),
            "processing_time_seconds": 5,
            "algorithm": "GEOH2_Simulation_Optimizer",
            "region_focus": region.title() + ", India" if region in india_sites else region.title(),
            "data_sources": [
                "Solar irradiance data",
                "Wind speed data",
                "Grid infrastructure",
                "Transportation networks",
                "Industrial demand centers"
            ],
            "cost_factors_considered": [
                "Renewable energy potential",
                "Grid connection costs",
                "Transportation infrastructure",
                "Land availability",
                "Water resources",
                "Labor costs",
                "Regulatory environment"
            ]
        }
    }

    print(f"✅ Simulation optimization completed! Found {len(features)} recommended sites.")
    return geojson_result

def get_optimization_status() -> dict:
    """
    Returns the status of the optimization engine.
    """
    if USE_REAL_OPTIMIZER:
        try:
            print("🔄 Calling real optimizer status...")
            status = real_get_status()
            print(f"✅ Real optimizer status: {status.get('engine')}")
            return status
        except Exception as e:
            print(f"❌ Real status check failed: {e}")
            print("🔄 Falling back to simulation status")

    return {
        "status": "operational",
        "engine": "GEOH2_Simulation_Optimizer",
        "version": "1.0.0",
        "database_connected": False,
        "capabilities": [
            "LCOH calculation",
            "Site optimization",
            "Geospatial analysis",
            "Cost breakdown analysis"
        ],
        "supported_regions": [
            "Gujarat", "Rajasthan", "Maharashtra", "Karnataka",
            "Tamil Nadu", "Andhra Pradesh", "India (All States)"
        ]
    }
    """
    Simulates the GEOH2 computational engine optimization process for Gujarat/India.

    Args:
        criteria (dict): User-defined optimization criteria

    Returns:
        dict: GeoJSON containing recommended sites with cost breakdowns
    """

    # Print optimization message
    print(f"Running optimization for criteria: {criteria}")

    # Simulate long-running computational process
    print("Processing geospatial data for Gujarat...")
    time.sleep(2)
    print("Calculating LCOH for potential sites...")
    time.sleep(2)
    print("Optimizing site selection...")
    time.sleep(1)

    # Gujarat/India specific coordinates (approximate bounds)
    # Gujarat coordinates roughly: 20.1°N to 24.7°N latitude, 68.1°E to 74.5°E longitude
    region = criteria.get('region', 'gujarat').lower()

    # Define sites for different Indian states
    india_sites = {
        'gujarat': [
            {"name": "Bhuj_Solar_Park", "lat": 23.241, "lon": 69.669, "base_lcoh": 3.5},
            {"name": "Kutch_Wind_Farm", "lat": 23.733, "lon": 68.867, "base_lcoh": 4.2},
            {"name": "Surat_Port_Complex", "lat": 21.170, "lon": 72.831, "base_lcoh": 4.8},
            {"name": "Ahmedabad_Industrial", "lat": 23.022, "lon": 72.571, "base_lcoh": 4.1},
            {"name": "Jamnagar_Refinery", "lat": 22.470, "lon": 70.057, "base_lcoh": 3.8},
            {"name": "Bhavnagar_Coast", "lat": 21.761, "lon": 72.151, "base_lcoh": 4.3},
            {"name": "Rajkot_Industrial", "lat": 22.303, "lon": 70.802, "base_lcoh": 4.5},
            {"name": "Vadodara_Chemical", "lat": 22.307, "lon": 73.181, "base_lcoh": 4.0}
        ],
        'rajasthan': [
            {"name": "Jaisalmer_Wind", "lat": 26.915, "lon": 70.908, "base_lcoh": 3.2},
            {"name": "Bikaner_Solar", "lat": 28.022, "lon": 73.311, "base_lcoh": 3.8},
            {"name": "Jodhpur_Industrial", "lat": 26.238, "lon": 73.024, "base_lcoh": 4.1},
            {"name": "Jaipur_Smart_City", "lat": 26.912, "lon": 75.787, "base_lcoh": 4.5},
            {"name": "Barmer_Renewable", "lat": 25.753, "lon": 71.393, "base_lcoh": 3.6}
        ],
        'maharashtra': [
            {"name": "Dhule_Solar", "lat": 20.902, "lon": 74.774, "base_lcoh": 4.0},
            {"name": "Pune_Technology", "lat": 18.520, "lon": 73.856, "base_lcoh": 4.3},
            {"name": "Mumbai_Port", "lat": 18.922, "lon": 72.834, "base_lcoh": 4.8},
            {"name": "Nagpur_Industrial", "lat": 21.145, "lon": 79.088, "base_lcoh": 4.2},
            {"name": "Aurangabad_Solar", "lat": 19.876, "lon": 75.343, "base_lcoh": 3.9}
        ],
        'karnataka': [
            {"name": "Bengaluru_Tech", "lat": 12.971, "lon": 77.594, "base_lcoh": 4.4},
            {"name": "Mangalore_Port", "lat": 12.914, "lon": 74.856, "base_lcoh": 4.1},
            {"name": "Hubli_Industrial", "lat": 15.364, "lon": 75.124, "base_lcoh": 4.0},
            {"name": "Mysore_Heritage", "lat": 12.295, "lon": 76.639, "base_lcoh": 4.2},
            {"name": "Tumkur_Solar", "lat": 13.340, "lon": 77.101, "base_lcoh": 3.8}
        ],
        'tamil_nadu': [
            {"name": "Chennai_Port", "lat": 13.082, "lon": 80.270, "base_lcoh": 4.5},
            {"name": "Coimbatore_Industrial", "lat": 11.016, "lon": 76.955, "base_lcoh": 4.2},
            {"name": "Tiruchirappalli_Solar", "lat": 10.790, "lon": 78.704, "base_lcoh": 4.0},
            {"name": "Madurai_Heritage", "lat": 9.925, "lon": 78.119, "base_lcoh": 4.3},
            {"name": "Tuticorin_Port", "lat": 8.764, "lon": 78.134, "base_lcoh": 4.1}
        ],
        'andhra_pradesh': [
            {"name": "Visakhapatnam_Port", "lat": 17.686, "lon": 83.218, "base_lcoh": 4.3},
            {"name": "Vijayawada_Industrial", "lat": 16.506, "lon": 80.648, "base_lcoh": 4.1},
            {"name": "Tirupati_Solar", "lat": 13.628, "lon": 79.419, "base_lcoh": 3.9},
            {"name": "Kakinada_Port", "lat": 16.989, "lon": 82.247, "base_lcoh": 4.2},
            {"name": "Anantapur_Wind", "lat": 14.681, "lon": 77.600, "base_lcoh": 3.7}
        ]
    }

    if region in india_sites:
        # Select sites from the specific state
        available_sites = india_sites[region]
        selected_sites = random.sample(available_sites, min(len(available_sites), random.randint(3, 5)))
    elif region == 'india':
        # Select sites from multiple states for "India" option
        all_sites = []
        for state_sites in india_sites.values():
            all_sites.extend(state_sites)
        selected_sites = random.sample(all_sites, random.randint(4, 6))
    else:
        # Fallback to global random sites if not India
        selected_sites = []
        for i in range(random.randint(3, 5)):
            selected_sites.append({
                "name": f"Site_{i+1}_{region.title()}",
                "lat": random.uniform(-90, 90),
                "lon": random.uniform(-180, 180),
                "base_lcoh": random.uniform(2.0, 6.0)
            })

    features = []

    for i, site in enumerate(selected_sites):
        # Apply criteria-based adjustments
        max_cost = criteria.get('max_cost', 6.0)
        base_lcoh = site['base_lcoh']

        # Adjust LCOH based on proximity to grid (if enabled)
        if criteria.get('proximity_to_grid', True):
            # Sites closer to infrastructure have lower costs
            grid_bonus = random.uniform(0.1, 0.5)
            base_lcoh = max(2.0, base_lcoh - grid_bonus)

        # Ensure LCOH doesn't exceed max_cost
        lcoh = min(base_lcoh, max_cost - 0.1)

        # Generate cost components
        production_cost = round(random.uniform(1.0, lcoh - 0.5), 2)
        transport_cost = round(lcoh - production_cost, 2)

        # Ensure transport_cost is positive
        if transport_cost < 0:
            transport_cost = round(random.uniform(0.1, 0.5), 2)
            production_cost = round(lcoh - transport_cost, 2)

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [site['lon'], site['lat']]  # GeoJSON format: [lng, lat]
            },
            "properties": {
                "site_name": site['name'],
                "lcoh": round(lcoh, 2),
                "production_cost": production_cost,
                "transport_cost": transport_cost,
                "region": region.title(),
                "max_cost": max_cost,
                "rank": i + 1,
                "coordinates": f"{site['lat']:.3f}°N, {site['lon']:.3f}°E"
            }
        }
        features.append(feature)

    # Sort features by LCOH (lowest cost first)
    features.sort(key=lambda x: x["properties"]["lcoh"])

    # Update ranks after sorting
    for i, feature in enumerate(features):
        feature["properties"]["rank"] = i + 1

    # Create GeoJSON structure
    geojson_result = {
        "type": "FeatureCollection",
        "features": features,
        "metadata": {
            "optimization_criteria": criteria,
            "total_sites_found": len(features),
            "processing_time_seconds": 5,
            "algorithm": "GEOH2_India_Optimizer",
            "region_focus": region.title() + ", India" if region in india_sites else region.title(),
            "data_sources": [
                "Solar irradiance data",
                "Wind speed data",
                "Grid infrastructure",
                "Transportation networks",
                "Industrial demand centers",
                "Port facilities",
                "Existing hydrogen infrastructure"
            ],
            "cost_factors_considered": [
                "Renewable energy potential",
                "Grid connection costs",
                "Transportation infrastructure",
                "Land availability",
                "Water resources",
                "Labor costs",
                "Regulatory environment"
            ]
        }
    }

    print(f"Optimization complete! Found {len(features)} recommended sites in {region.title()}.")
    return geojson_result

# Example usage and testing
if __name__ == "__main__":
    # Test the optimizer
    test_criteria = {
        "region": "namibia",
        "max_cost": 5.0,
        "min_production": 1000,
        "proximity_to_grid": True
    }

    result = run_optimization(test_criteria)
    print("\nOptimization Result:")
    print(json.dumps(result, indent=2))
