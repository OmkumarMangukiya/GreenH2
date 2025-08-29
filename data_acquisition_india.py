#!/usr/bin/env python3
"""
Data Acquisition Script for Indian States - GreenH2 Project
Downloads and processes geospatial data for renewable energy optimization
"""

import requests
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import os
import json
from pathlib import Path

class IndiaDataDownloader:
    def __init__(self, data_dir="data/india"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def download_state_boundaries(self):
        """Download Indian state boundaries from Natural Earth"""
        print("Downloading Indian state boundaries...")

        # Natural Earth Admin 1 boundaries (includes Indian states)
        url = "https://naturalearth.s3.amazonaws.com/10m_cultural/ne_10m_admin_1_states_provinces.zip"

        try:
            import zipfile
            import io

            response = requests.get(url)
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                z.extractall(self.data_dir / "boundaries")

            # Filter for India
            boundaries_file = self.data_dir / "boundaries" / "ne_10m_admin_1_states_provinces.shp"
            if boundaries_file.exists():
                gdf = gpd.read_file(boundaries_file)
                india_states = gdf[gdf['ADM0_NAME'] == 'India']
                india_states.to_file(self.data_dir / "boundaries" / "india_states.geojson", driver='GeoJSON')
                print(f"Downloaded {len(india_states)} Indian states")

        except Exception as e:
            print(f"Error downloading boundaries: {e}")

    def download_solar_data(self):
        """Download solar irradiance data from NASA POWER"""
        print("Downloading solar irradiance data...")

        # NASA POWER API for solar data
        base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"

        # Major cities coordinates for sample data
        locations = {
            'Mumbai': (19.0760, 72.8777),
            'Delhi': (28.7041, 77.1025),
            'Bangalore': (12.9716, 77.5946),
            'Chennai': (13.0827, 80.2707),
            'Kolkata': (22.5726, 88.3639),
            'Ahmedabad': (23.0225, 72.5714),
            'Pune': (18.5204, 73.8567),
            'Jaipur': (26.9124, 75.7873),
            'Bhuj': (23.2410, 69.6669),  # Gujarat solar hub
            'Jaisalmer': (26.9157, 70.9083),  # Rajasthan solar hub
            'Dhule': (20.9042, 74.7749),  # Maharashtra solar hub
            'Tumkur': (13.3409, 77.1000),  # Karnataka solar hub
            'Tirupati': (13.6288, 79.4192),  # Andhra Pradesh solar hub
            'Coimbatore': (11.0168, 76.9558)  # Tamil Nadu solar hub
        }

        solar_data = []

        for city, (lat, lon) in locations.items():
            try:
                params = {
                    'start': '20230101',
                    'end': '20231231',
                    'latitude': lat,
                    'longitude': lon,
                    'community': 'RE',
                    'parameters': 'ALLSKY_SFC_SW_DWN',  # Solar irradiance
                    'format': 'JSON'
                }

                response = requests.get(base_url, params=params)
                data = response.json()

                if 'properties' in data:
                    irradiance = data['properties']['parameter']['ALLSKY_SFC_SW_DWN']
                    avg_irradiance = sum(irradiance.values()) / len(irradiance)

                    solar_data.append({
                        'city': city,
                        'latitude': lat,
                        'longitude': lon,
                        'avg_solar_irradiance_kwh_m2_day': avg_irradiance / 1000,  # Convert to kWh/m²/day
                        'state': self.get_state_from_city(city)
                    })

                print(f"Downloaded solar data for {city}")

            except Exception as e:
                print(f"Error downloading solar data for {city}: {e}")

        # Save to CSV
        df = pd.DataFrame(solar_data)
        df.to_csv(self.data_dir / "solar_irradiance_india.csv", index=False)
        print(f"Saved solar data for {len(solar_data)} locations")

    def download_wind_data(self):
        """Download wind speed data from Global Wind Atlas"""
        print("Downloading wind speed data...")

        # Sample wind data for Indian states (based on known wind corridors)
        wind_data = [
            {'state': 'Gujarat', 'city': 'Bhuj', 'latitude': 23.2410, 'longitude': 69.6669, 'wind_speed_ms': 6.2},
            {'state': 'Rajasthan', 'city': 'Jaisalmer', 'latitude': 26.9157, 'longitude': 70.9083, 'wind_speed_ms': 5.8},
            {'state': 'Maharashtra', 'city': 'Dhule', 'latitude': 20.9042, 'longitude': 74.7749, 'wind_speed_ms': 4.9},
            {'state': 'Karnataka', 'city': 'Tumkur', 'latitude': 13.3409, 'longitude': 77.1000, 'wind_speed_ms': 5.1},
            {'state': 'Tamil Nadu', 'city': 'Coimbatore', 'latitude': 11.0168, 'longitude': 76.9558, 'wind_speed_ms': 4.7},
            {'state': 'Andhra Pradesh', 'city': 'Tirupati', 'latitude': 13.6288, 'longitude': 79.4192, 'wind_speed_ms': 4.3},
            {'state': 'Madhya Pradesh', 'city': 'Indore', 'latitude': 22.7196, 'longitude': 75.8577, 'wind_speed_ms': 3.8},
            {'state': 'Kerala', 'city': 'Kochi', 'latitude': 9.9312, 'longitude': 76.2673, 'wind_speed_ms': 3.2},
        ]

        df = pd.DataFrame(wind_data)
        df.to_csv(self.data_dir / "wind_speed_india.csv", index=False)
        print(f"Saved wind data for {len(wind_data)} locations")

    def download_infrastructure_data(self):
        """Download infrastructure data (ports, industrial parks)"""
        print("Creating infrastructure data...")

        # Major ports in India
        ports = [
            {'name': 'Jawaharlal Nehru Port', 'state': 'Maharashtra', 'latitude': 18.9492, 'longitude': 72.9322, 'capacity_mw': 500},
            {'name': 'Mumbai Port', 'state': 'Maharashtra', 'latitude': 18.9207, 'longitude': 72.8347, 'capacity_mw': 300},
            {'name': 'Chennai Port', 'state': 'Tamil Nadu', 'latitude': 13.0827, 'longitude': 80.2707, 'capacity_mw': 400},
            {'name': 'Kolkata Port', 'state': 'West Bengal', 'latitude': 22.5726, 'longitude': 88.3639, 'capacity_mw': 350},
            {'name': 'Visakhapatnam Port', 'state': 'Andhra Pradesh', 'latitude': 17.6868, 'longitude': 83.2185, 'capacity_mw': 450},
            {'name': 'Cochin Port', 'state': 'Kerala', 'latitude': 9.9312, 'longitude': 76.2673, 'capacity_mw': 250},
            {'name': 'Mangalore Port', 'state': 'Karnataka', 'latitude': 12.9141, 'longitude': 74.8143, 'capacity_mw': 200},
            {'name': 'Jamnagar Port', 'state': 'Gujarat', 'latitude': 22.4707, 'longitude': 70.0577, 'capacity_mw': 600},
            {'name': 'Mundra Port', 'state': 'Gujarat', 'latitude': 22.8397, 'longitude': 69.7258, 'capacity_mw': 550},
            {'name': 'Tuticorin Port', 'state': 'Tamil Nadu', 'latitude': 8.7642, 'longitude': 78.1348, 'capacity_mw': 300},
        ]

        # Industrial parks and special economic zones
        industrial_parks = [
            {'name': 'Taloja Industrial Area', 'state': 'Maharashtra', 'latitude': 19.0833, 'longitude': 73.1000, 'capacity_mw': 200},
            {'name': 'Pune IT Park', 'state': 'Maharashtra', 'latitude': 18.5204, 'longitude': 73.8567, 'capacity_mw': 150},
            {'name': 'Bengaluru Tech Park', 'state': 'Karnataka', 'latitude': 12.9716, 'longitude': 77.5946, 'capacity_mw': 300},
            {'name': 'Chennai Tidel Park', 'state': 'Tamil Nadu', 'latitude': 12.9814, 'longitude': 80.2180, 'capacity_mw': 250},
            {'name': 'Vadodara Chemical Hub', 'state': 'Gujarat', 'latitude': 22.3072, 'longitude': 73.1812, 'capacity_mw': 400},
            {'name': 'Jodhpur Industrial Area', 'state': 'Rajasthan', 'latitude': 26.2389, 'longitude': 73.0243, 'capacity_mw': 180},
            {'name': 'Vijayawada Industrial Park', 'state': 'Andhra Pradesh', 'latitude': 16.5062, 'longitude': 80.6480, 'capacity_mw': 220},
        ]

        # Combine and save
        infrastructure_data = []
        for port in ports:
            infrastructure_data.append({
                'facility_name': port['name'],
                'facility_type': 'port',
                'state': port['state'],
                'latitude': port['latitude'],
                'longitude': port['longitude'],
                'capacity_mw': port['capacity_mw'],
                'status': 'operational'
            })

        for park in industrial_parks:
            infrastructure_data.append({
                'facility_name': park['name'],
                'facility_type': 'industrial_park',
                'state': park['state'],
                'latitude': park['latitude'],
                'longitude': park['longitude'],
                'capacity_mw': park['capacity_mw'],
                'status': 'operational'
            })

        df = pd.DataFrame(infrastructure_data)
        df.to_csv(self.data_dir / "infrastructure_india.csv", index=False)
        print(f"Saved infrastructure data for {len(infrastructure_data)} facilities")

    def get_state_from_city(self, city):
        """Map city to state"""
        city_state_map = {
            'Mumbai': 'Maharashtra', 'Pune': 'Maharashtra', 'Dhule': 'Maharashtra',
            'Delhi': 'Delhi', 'Jaipur': 'Rajasthan', 'Jaisalmer': 'Rajasthan',
            'Bangalore': 'Karnataka', 'Tumkur': 'Karnataka',
            'Chennai': 'Tamil Nadu', 'Coimbatore': 'Tamil Nadu', 'Tirupati': 'Tamil Nadu',
            'Kolkata': 'West Bengal',
            'Ahmedabad': 'Gujarat', 'Bhuj': 'Gujarat',
            'Tirupati': 'Andhra Pradesh'
        }
        return city_state_map.get(city, 'Unknown')

    def create_sample_renewable_potential_data(self):
        """Create sample renewable potential data for database"""
        print("Creating sample renewable potential data...")

        # Combine solar and wind data
        solar_df = pd.read_csv(self.data_dir / "solar_irradiance_india.csv")
        wind_df = pd.read_csv(self.data_dir / "wind_speed_india.csv")

        renewable_data = []

        for _, row in solar_df.iterrows():
            # Find matching wind data or use default
            wind_match = wind_df[wind_df['state'] == row['state']]
            wind_speed = wind_match['wind_speed_ms'].iloc[0] if not wind_match.empty else 4.0

            renewable_data.append({
                'site_name': f"{row['city']} Solar Park",
                'state': row['state'],
                'latitude': row['latitude'],
                'longitude': row['longitude'],
                'solar_irradiance': row['avg_solar_irradiance_kwh_m2_day'],
                'wind_speed': wind_speed,
                'land_suitability': 0.8,  # Assume good suitability
                'grid_distance_km': 25.0  # Assume average distance
            })

        df = pd.DataFrame(renewable_data)
        df.to_csv(self.data_dir / "renewable_potential_india.csv", index=False)
        print(f"Created renewable potential data for {len(renewable_data)} sites")

    def download_all_data(self):
        """Download all required data"""
        print("Starting comprehensive data download for India...")

        self.download_state_boundaries()
        self.download_solar_data()
        self.download_wind_data()
        self.download_infrastructure_data()
        self.create_sample_renewable_potential_data()

        print("\nData download complete!")
        print(f"Files saved in: {self.data_dir}")
        print("\nGenerated files:")
        for file in self.data_dir.rglob("*.csv"):
            print(f"- {file.name}")
        for file in self.data_dir.rglob("*.geojson"):
            print(f"- {file.name}")

if __name__ == "__main__":
    downloader = IndiaDataDownloader()
    downloader.download_all_data()
