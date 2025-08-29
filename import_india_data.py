#!/usr/bin/env python3
"""
Import India Data into PostGIS Database
Loads the downloaded CSV data into your GreenH2 database
"""

import psycopg2
import csv
import json
from pathlib import Path

def import_renewable_potential_data(cursor, data_dir):
    """Import renewable potential data into database"""
    print("Importing renewable potential data...")

    with open(data_dir / "renewable_potential_india.csv", 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("""
                INSERT INTO renewable_potential (
                    location_name, state, coordinates, solar_irradiance_kwh_m2_day,
                    wind_speed_ms, land_suitability_score, grid_distance_km
                ) VALUES (%s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s, %s, %s, %s)
            """, (
                row['site_name'],
                row['state'],
                float(row['longitude']),
                float(row['latitude']),
                float(row['solar_irradiance']),
                float(row['wind_speed']),
                float(row['land_suitability']),
                float(row['grid_distance_km'])
            ))

    print("✓ Renewable potential data imported")

def import_infrastructure_data(cursor, data_dir):
    """Import infrastructure data into database"""
    print("Importing infrastructure data...")

    with open(data_dir / "infrastructure_india.csv", 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("""
                INSERT INTO infrastructure (
                    facility_name, facility_type, state, coordinates,
                    capacity_mw, status
                ) VALUES (%s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s, %s)
            """, (
                row['facility_name'],
                row['facility_type'],
                row['state'],
                float(row['longitude']),
                float(row['latitude']),
                float(row['capacity_mw']),
                row['status']
            ))

    print("✓ Infrastructure data imported")

def import_transportation_data(cursor, data_dir):
    """Import transportation network data into database"""
    print("Importing transportation network data...")

    with open(data_dir / "transportation_india.csv", 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Create a simple linestring from the point (for demo purposes)
            # In production, you'd have actual line geometries
            cursor.execute("""
                INSERT INTO transportation_network (
                    segment_name, network_type, state,
                    geometry, capacity_tonnes_year, status
                ) VALUES (%s, %s, %s,
                    ST_SetSRID(ST_MakeLine(ST_MakePoint(%s, %s), ST_MakePoint(%s, %s)), 4326),
                    %s, %s)
            """, (
                row['network_name'],
                row['network_type'],
                row['state'],
                float(row['longitude']) - 0.01, float(row['latitude']) - 0.01,  # Start point
                float(row['longitude']) + 0.01, float(row['latitude']) + 0.01,  # End point
                float(row['capacity_tonnes_year']),
                row['status']
            ))

    print("✓ Transportation network data imported")

def main():
    """Main function to import all data"""
    data_dir = Path("data/india")

    if not data_dir.exists():
        print("❌ Data directory not found. Run simple_data_downloader.py first")
        return

    # Database connection parameters
    db_params = {
        'dbname': 'greenh2_db',
        'user': 'omman',
        'password': 'greenh2_password',
        'host': 'localhost',
        'port': '5432'
    }

    try:
        print("Connecting to database...")
        conn = psycopg2.connect(**db_params)
        conn.autocommit = True
        cursor = conn.cursor()

        print("✅ Connected to database successfully!")

        # Import all data
        import_renewable_potential_data(cursor, data_dir)
        import_infrastructure_data(cursor, data_dir)
        import_transportation_data(cursor, data_dir)

        # Create spatial indexes for better performance
        print("Creating spatial indexes...")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_renewable_potential_geom ON renewable_potential USING GIST (coordinates);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_infrastructure_geom ON infrastructure USING GIST (coordinates);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_transportation_geom ON transportation_network USING GIST (geometry);")

        print("✅ Spatial indexes created")

        # Show summary
        cursor.execute("SELECT COUNT(*) FROM renewable_potential;")
        renewable_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM infrastructure;")
        infra_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM transportation_network;")
        transport_count = cursor.fetchone()[0]

        print("\n📊 Data Import Summary:")
        print(f"   Renewable potential sites: {renewable_count}")
        print(f"   Infrastructure facilities: {infra_count}")
        print(f"   Transportation networks: {transport_count}")
        print(f"   Total records: {renewable_count + infra_count + transport_count}")

        cursor.close()
        conn.close()

        print("\n🎉 Data import complete!")
        print("Your GreenH2 database now has Indian geospatial data ready for optimization!")

    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        print("Make sure:")
        print("1. PostgreSQL is running")
        print("2. Database 'greenh2_db' exists")
        print("3. User 'omman' has access")
        print("4. PostGIS extension is enabled")

    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        print("Run simple_data_downloader.py first to generate the data files")

if __name__ == "__main__":
    main()
