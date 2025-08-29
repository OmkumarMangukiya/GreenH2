#!/usr/bin/env python3
"""
Simple India Data Downloader - No heavy dependencies required
Downloads basic geospatial data for Indian states
"""

import requests
import json
import csv
import os
from pathlib import Path

class SimpleIndiaDataDownloader:
    def __init__(self, data_dir="data/india"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def download_state_boundaries(self):
        """Download simplified Indian state boundaries"""
        print("Downloading Indian state boundaries...")

        # Using a simplified GeoJSON source for Indian states
        # This is a basic representation - for production use proper GIS data
        india_states = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"name": "Gujarat", "region": "Western India"},
                    "geometry": {"type": "Point", "coordinates": [71.1924, 22.2587]}
                },
                {
                    "type": "Feature",
                    "properties": {"name": "Rajasthan", "region": "Northern India"},
                    "geometry": {"type": "Point", "coordinates": [74.2179, 27.0238]}
                },
                {
                    "type": "Feature",
                    "properties": {"name": "Maharashtra", "region": "Western India"},
                    "geometry": {"type": "Point", "coordinates": [75.7139, 19.7515]}
                },
                {
                    "type": "Feature",
                    "properties": {"name": "Karnataka", "region": "Southern India"},
                    "geometry": {"type": "Point", "coordinates": [75.7139, 15.3173]}
                },
                {
                    "type": "Feature",
                    "properties": {"name": "Tamil Nadu", "region": "Southern India"},
                    "geometry": {"type": "Point", "coordinates": [78.6569, 11.1271]}
                },
                {
                    "type": "Feature",
                    "properties": {"name": "Andhra Pradesh", "region": "Southern India"},
                    "geometry": {"type": "Point", "coordinates": [79.7400, 15.9129]}
                }
            ]
        }

        with open(self.data_dir / "india_states_simple.geojson", 'w') as f:
            json.dump(india_states, f, indent=2)

        print("Created simplified Indian states data")

    def create_renewable_energy_data(self):
        """Create sample renewable energy data for Indian states"""
        print("Creating renewable energy potential data...")

        renewable_data = [
            # Gujarat - High solar potential
            {"state": "Gujarat", "site_name": "Bhuj Solar Park", "latitude": 23.2410, "longitude": 69.6669,
             "solar_irradiance": 5.8, "wind_speed": 6.2, "land_suitability": 0.9, "grid_distance_km": 15.0},
            {"state": "Gujarat", "site_name": "Kutch Wind Farm", "latitude": 23.7337, "longitude": 68.8647,
             "solar_irradiance": 5.6, "wind_speed": 7.1, "land_suitability": 0.8, "grid_distance_km": 20.0},

            # Rajasthan - High solar and wind
            {"state": "Rajasthan", "site_name": "Jaisalmer Solar Park", "latitude": 26.9157, "longitude": 70.9083,
             "solar_irradiance": 6.2, "wind_speed": 5.8, "land_suitability": 0.9, "grid_distance_km": 25.0},
            {"state": "Rajasthan", "site_name": "Bikaner Wind Park", "latitude": 28.0229, "longitude": 73.3119,
             "solar_irradiance": 5.9, "wind_speed": 6.5, "land_suitability": 0.8, "grid_distance_km": 30.0},

            # Maharashtra - Good solar and moderate wind
            {"state": "Maharashtra", "site_name": "Dhule Solar Park", "latitude": 20.9042, "longitude": 74.7749,
             "solar_irradiance": 5.4, "wind_speed": 4.9, "land_suitability": 0.8, "grid_distance_km": 18.0},
            {"state": "Maharashtra", "site_name": "Solapur Wind Farm", "latitude": 17.6599, "longitude": 75.9064,
             "solar_irradiance": 5.2, "wind_speed": 5.2, "land_suitability": 0.7, "grid_distance_km": 22.0},

            # Karnataka - Good solar potential
            {"state": "Karnataka", "site_name": "Tumkur Solar Park", "latitude": 13.3409, "longitude": 77.1000,
             "solar_irradiance": 5.3, "wind_speed": 5.1, "land_suitability": 0.8, "grid_distance_km": 20.0},
            {"state": "Karnataka", "site_name": "Pavagada Solar Park", "latitude": 14.1000, "longitude": 77.2833,
             "solar_irradiance": 5.5, "wind_speed": 4.8, "land_suitability": 0.9, "grid_distance_km": 15.0},

            # Tamil Nadu - Good solar and coastal wind
            {"state": "Tamil Nadu", "site_name": "Kamuthi Solar Power Project", "latitude": 9.4043, "longitude": 78.3734,
             "solar_irradiance": 5.6, "wind_speed": 4.7, "land_suitability": 0.8, "grid_distance_km": 12.0},
            {"state": "Tamil Nadu", "site_name": "Muppandal Wind Farm", "latitude": 8.2667, "longitude": 77.5167,
             "solar_irradiance": 5.1, "wind_speed": 6.8, "land_suitability": 0.7, "grid_distance_km": 8.0},

            # Andhra Pradesh - High solar potential
            {"state": "Andhra Pradesh", "site_name": "Anantapur Solar Park", "latitude": 14.6819, "longitude": 77.6006,
             "solar_irradiance": 5.7, "wind_speed": 4.3, "land_suitability": 0.9, "grid_distance_km": 18.0},
            {"state": "Andhra Pradesh", "site_name": "Kurnool Ultra Mega Solar Park", "latitude": 15.8281, "longitude": 78.0373,
             "solar_irradiance": 5.8, "wind_speed": 4.1, "land_suitability": 0.9, "grid_distance_km": 20.0},
        ]

        with open(self.data_dir / "renewable_potential_india.csv", 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=renewable_data[0].keys())
            writer.writeheader()
            writer.writerows(renewable_data)

        print(f"Created renewable potential data for {len(renewable_data)} sites")

    def create_infrastructure_data(self):
        """Create sample infrastructure data"""
        print("Creating infrastructure data...")

        infrastructure_data = [
            # Ports
            {"facility_name": "Jamnagar Port", "facility_type": "port", "state": "Gujarat",
             "latitude": 22.4707, "longitude": 70.0577, "capacity_mw": 600, "status": "operational"},
            {"facility_name": "Mumbai Port", "facility_type": "port", "state": "Maharashtra",
             "latitude": 18.9207, "longitude": 72.8347, "capacity_mw": 300, "status": "operational"},
            {"facility_name": "Chennai Port", "facility_type": "port", "state": "Tamil Nadu",
             "latitude": 13.0827, "longitude": 80.2707, "capacity_mw": 400, "status": "operational"},
            {"facility_name": "Visakhapatnam Port", "facility_type": "port", "state": "Andhra Pradesh",
             "latitude": 17.6868, "longitude": 83.2185, "capacity_mw": 450, "status": "operational"},
            {"facility_name": "Mangalore Port", "facility_type": "port", "state": "Karnataka",
             "latitude": 12.9141, "longitude": 74.8143, "capacity_mw": 200, "status": "operational"},

            # Industrial Parks
            {"facility_name": "Vadodara Chemical Hub", "facility_type": "industrial_park", "state": "Gujarat",
             "latitude": 22.3072, "longitude": 73.1812, "capacity_mw": 400, "status": "operational"},
            {"facility_name": "Taloja Industrial Area", "facility_type": "industrial_park", "state": "Maharashtra",
             "latitude": 19.0833, "longitude": 73.1000, "capacity_mw": 200, "status": "operational"},
            {"facility_name": "Bengaluru Tech Park", "facility_type": "industrial_park", "state": "Karnataka",
             "latitude": 12.9716, "longitude": 77.5946, "capacity_mw": 300, "status": "operational"},
            {"facility_name": "Chennai Tidel Park", "facility_type": "industrial_park", "state": "Tamil Nadu",
             "latitude": 12.9814, "longitude": 80.2180, "capacity_mw": 250, "status": "operational"},
            {"facility_name": "Vijayawada Industrial Park", "facility_type": "industrial_park", "state": "Andhra Pradesh",
             "latitude": 16.5062, "longitude": 80.6480, "capacity_mw": 220, "status": "operational"},

            # Substations (sample)
            {"facility_name": "Bhuj Substation", "facility_type": "substation", "state": "Gujarat",
             "latitude": 23.2410, "longitude": 69.6669, "capacity_mw": 500, "status": "operational"},
            {"facility_name": "Jaisalmer Substation", "facility_type": "substation", "state": "Rajasthan",
             "latitude": 26.9157, "longitude": 70.9083, "capacity_mw": 400, "status": "operational"},
            {"facility_name": "Dhule Substation", "facility_type": "substation", "state": "Maharashtra",
             "latitude": 20.9042, "longitude": 74.7749, "capacity_mw": 300, "status": "operational"},
        ]

        with open(self.data_dir / "infrastructure_india.csv", 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=infrastructure_data[0].keys())
            writer.writeheader()
            writer.writerows(infrastructure_data)

        print(f"Created infrastructure data for {len(infrastructure_data)} facilities")

    def create_transportation_data(self):
        """Create sample transportation network data"""
        print("Creating transportation network data...")

        transportation_data = [
            # Major highways
            {"network_name": "NH-48 (Golden Quadrilateral)", "network_type": "road", "state": "Maharashtra",
             "latitude": 19.0760, "longitude": 72.8777, "capacity_tonnes_year": 5000000, "status": "operational"},
            {"network_name": "NH-8 (Delhi-Mumbai)", "network_type": "road", "state": "Rajasthan",
             "latitude": 26.9124, "longitude": 75.7873, "capacity_tonnes_year": 3000000, "status": "operational"},
            {"network_name": "NH-44 (North-South Corridor)", "network_type": "road", "state": "Karnataka",
             "latitude": 12.9716, "longitude": 77.5946, "capacity_tonnes_year": 4000000, "status": "operational"},

            # Railways
            {"network_name": "Western Railway", "network_type": "rail", "state": "Gujarat",
             "latitude": 23.0225, "longitude": 72.5714, "capacity_tonnes_year": 10000000, "status": "operational"},
            {"network_name": "Southern Railway", "network_type": "rail", "state": "Tamil Nadu",
             "latitude": 13.0827, "longitude": 80.2707, "capacity_tonnes_year": 8000000, "status": "operational"},
            {"network_name": "South Central Railway", "network_type": "rail", "state": "Andhra Pradesh",
             "latitude": 17.6868, "longitude": 83.2185, "capacity_tonnes_year": 9000000, "status": "operational"},
        ]

        with open(self.data_dir / "transportation_india.csv", 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=transportation_data[0].keys())
            writer.writeheader()
            writer.writerows(transportation_data)

        print(f"Created transportation data for {len(transportation_data)} networks")

    def download_all_data(self):
        """Download all basic data"""
        print("Starting basic India data download...")
        print("This creates sample data for development and testing")
        print("For production use, download real data from government sources\n")

        self.download_state_boundaries()
        self.create_renewable_energy_data()
        self.create_infrastructure_data()
        self.create_transportation_data()

        print("\nData download complete!")
        print(f"Files saved in: {self.data_dir}")
        print("\nGenerated files:")
        for file in self.data_dir.rglob("*.csv"):
            print(f"- {file.name}")
        for file in self.data_dir.rglob("*.geojson"):
            print(f"- {file.name}")

        print("\nNext steps:")
        print("1. Review the generated CSV files")
        print("2. Import data into your PostGIS database")
        print("3. For production: Download real data from government sources")
        print("4. See INDIA_DATA_SOURCES.md for detailed data acquisition guide")

if __name__ == "__main__":
    downloader = SimpleIndiaDataDownloader()
    downloader.download_all_data()
