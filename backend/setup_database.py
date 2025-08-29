#!/usr/bin/env python3
"""
Database setup script for GreenH2
Creates tables for storing geospatial data and optimization results
"""

import psycopg2
from psycopg2 import sql

def create_database_schema():
    """Create the database schema for GreenH2"""

    # Database connection parameters
    db_params = {
        'dbname': 'greenh2_db',
        'user': 'omman',  # Replace with your username
        'password': 'greenh2_password',   # PostgreSQL password
        'host': 'localhost',
        'port': '5432'
    }

    try:
        # Connect to database
        conn = psycopg2.connect(**db_params)
        conn.autocommit = True
        cursor = conn.cursor()

        print("Connected to database successfully!")

        # Create renewable energy potential table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS renewable_potential (
                id SERIAL PRIMARY KEY,
                location_name VARCHAR(255),
                state VARCHAR(100),
                coordinates GEOMETRY(POINT, 4326),
                solar_irradiance_kwh_m2_day FLOAT,
                wind_speed_ms FLOAT,
                land_suitability_score FLOAT,
                grid_distance_km FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Create infrastructure table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS infrastructure (
                id SERIAL PRIMARY KEY,
                facility_type VARCHAR(100), -- 'port', 'industrial_park', 'substation', etc.
                facility_name VARCHAR(255),
                state VARCHAR(100),
                coordinates GEOMETRY(POINT, 4326),
                capacity_mw FLOAT,
                status VARCHAR(50), -- 'existing', 'planned', 'proposed'
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Create transportation network table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transportation_network (
                id SERIAL PRIMARY KEY,
                network_type VARCHAR(100), -- 'road', 'rail', 'pipeline'
                segment_name VARCHAR(255),
                state VARCHAR(100),
                geometry GEOMETRY(LINESTRING, 4326),
                capacity_tonnes_year FLOAT,
                status VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Create optimization results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS optimization_results (
                id SERIAL PRIMARY KEY,
                run_id VARCHAR(100),
                site_name VARCHAR(255),
                state VARCHAR(100),
                coordinates GEOMETRY(POINT, 4326),
                lcoh_usd_kg FLOAT,
                production_cost_usd_kg FLOAT,
                transport_cost_usd_kg FLOAT,
                total_capacity_tonnes_year FLOAT,
                renewable_mix JSONB, -- {'solar': 0.7, 'wind': 0.3}
                criteria_used JSONB,
                rank INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Create spatial indexes for better performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_renewable_potential_coords ON renewable_potential USING GIST (coordinates);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_infrastructure_coords ON infrastructure USING GIST (coordinates);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_transportation_geom ON transportation_network USING GIST (geometry);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_optimization_coords ON optimization_results USING GIST (coordinates);")

        print("Database schema created successfully!")

        # Insert sample data for Indian states
        insert_sample_data(cursor)

        cursor.close()
        conn.close()
        print("Database setup completed!")

    except Exception as e:
        print(f"Error setting up database: {e}")
        return False

    return True

def insert_sample_data(cursor):
    """Insert sample geospatial data for Indian states"""

    # Sample renewable energy potential data
    renewable_data = [
        ('Bhuj Solar Park', 'Gujarat', 23.241, 69.669, 6.2, 7.8, 0.85, 15.2),
        ('Kutch Wind Farm', 'Gujarat', 23.733, 68.867, 5.8, 8.5, 0.90, 8.5),
        ('Jaisalmer Solar', 'Rajasthan', 26.915, 70.908, 6.8, 6.2, 0.95, 25.0),
        ('Bikaner Wind', 'Rajasthan', 28.022, 73.311, 5.5, 7.1, 0.88, 18.3),
        ('Dhule Solar', 'Maharashtra', 20.902, 74.774, 5.9, 6.8, 0.82, 12.1),
        ('Pune Wind', 'Maharashtra', 18.520, 73.856, 5.2, 5.9, 0.75, 22.4),
        ('Bengaluru Solar', 'Karnataka', 12.971, 77.594, 5.6, 5.2, 0.78, 8.9),
        ('Mangalore Wind', 'Karnataka', 12.914, 74.856, 5.1, 6.1, 0.85, 5.2),
        ('Chennai Solar', 'Tamil Nadu', 13.082, 80.270, 5.7, 5.8, 0.80, 14.7),
        ('Coimbatore Wind', 'Tamil Nadu', 11.016, 76.955, 5.3, 6.5, 0.83, 9.3),
        ('Visakhapatnam Solar', 'Andhra Pradesh', 17.686, 83.218, 5.8, 6.2, 0.87, 11.8),
        ('Tirupati Wind', 'Andhra Pradesh', 13.628, 79.419, 5.4, 5.7, 0.84, 16.2)
    ]

    cursor.executemany("""
        INSERT INTO renewable_potential
        (location_name, state, coordinates, solar_irradiance_kwh_m2_day, wind_speed_ms,
         land_suitability_score, grid_distance_km)
        VALUES (%s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s, %s, %s, %s)
    """, renewable_data)

    # Sample infrastructure data
    infrastructure_data = [
        ('Port', 'Jamnagar Port', 'Gujarat', 22.470, 70.057, 50000, 'existing'),
        ('Industrial Park', 'Ahmedabad Industrial Zone', 'Gujarat', 23.022, 72.571, 25000, 'existing'),
        ('Port', 'Mumbai Port', 'Maharashtra', 18.922, 72.834, 75000, 'existing'),
        ('Industrial Park', 'Pune IT Park', 'Maharashtra', 18.520, 73.856, 30000, 'existing'),
        ('Port', 'Chennai Port', 'Tamil Nadu', 13.082, 80.270, 65000, 'existing'),
        ('Industrial Park', 'Bengaluru Tech Park', 'Karnataka', 12.971, 77.594, 35000, 'existing')
    ]

    cursor.executemany("""
        INSERT INTO infrastructure
        (facility_type, facility_name, state, coordinates, capacity_mw, status)
        VALUES (%s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s, %s)
    """, infrastructure_data)

    print("Sample data inserted successfully!")

if __name__ == "__main__":
    create_database_schema()
