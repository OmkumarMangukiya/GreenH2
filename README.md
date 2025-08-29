# GreenH2

# GreenH2

An interactive, data-driven platform for optimizing green hydrogen infrastructure investments.

**GreenH2** is a full-stack web application designed to solve the critical challenge of strategic infrastructure placement. It provides urban planners, energy companies, and policy analysts with an intuitive, map-based tool to identify the most cost-effective and high-impact locations for new green hydrogen projects.

---

## Key Features

### 🌍 Interactive Map Interface

- A user-friendly, responsive map built with **React Leaflet**.
- Dynamic centering based on selected region (Gujarat, Rajasthan, Maharashtra, etc.)
- Users can pan, zoom, and click on markers for detailed information.

### 🗂️ Layered Data Visualization

Toggle multiple data layers on and off to gain a comprehensive geospatial understanding. Layers include:

- Existing/Planned Hydrogen Assets (Plants, Storage, Pipelines)
- Renewable Energy Potential (Solar Irradiance, Wind Speed)
- High-Capacity Grid Infrastructure
- Major Demand Centers (Industrial Hubs, Ports)
- Transport & Logistics Networks (Roads, Rail)

### ⚙️ Advanced Optimization Engine

- **Real GEOH2 Computational Core** with actual LCOH calculations
- **PostGIS Database** for efficient geospatial querying
- **Multi-criteria optimization** using real cost parameters
- **Infrastructure proximity analysis** for cost optimization
- **Levelized Cost of Hydrogen (LCOH)** calculations using industry-standard formulas

### 📊 Scenario-Based Site Recommendations

- Define investment criteria (e.g., proximity to solar, distance to port, target production cost)
- Support for **6 major Indian states**: Gujarat, Rajasthan, Maharashtra, Karnataka, Tamil Nadu, Andhra Pradesh
- **Real coordinates** for actual industrial locations
- Receive a ranked list of optimal project locations highlighted on the map

### 📈 Dynamic Results Display

- Clicking a recommended site shows detailed cost breakdowns
- **Production costs**, **transport costs**, and **infrastructure proximity**
- **Annual production capacity** and **renewable potential scores**
- **Real-time optimization** with database-driven results

---

## Tech Stack

- **Frontend:** React, React Leaflet, TypeScript, Tailwind CSS
- **Backend API:** Python (FastAPI)
- **Database:** PostgreSQL with PostGIS extension
- **Computational Engine:** Custom GEOH2 Optimizer (Python with geospatial analysis)
- **Geospatial Libraries:** GeoPandas, Shapely, Rasterio
- **Optimization Libraries:** NumPy, Pandas, SciPy

---

## How It Works

1. **User Interaction**
   Define an area of interest and set criteria (e.g., _"Find the cheapest locations for a new plant in Gujarat close to the grid"_) via the web interface.

2. **API Request**
   React frontend sends a structured request to the FastAPI backend.

3. **Database Query**
   Backend queries PostGIS database for renewable potential and infrastructure data.

4. **Optimization Processing**
   GEOH2 computational engine:

   - Calculates renewable energy potential scores
   - Analyzes infrastructure proximity
   - Computes LCOH using real cost parameters
   - Applies multi-criteria optimization

5. **Data Processing**
   The engine processes geospatial data, runs LCOH optimization, and calculates the best sites using:

   - Haversine distance calculations
   - Cost-benefit analysis
   - Infrastructure proximity bonuses
   - Land suitability factors

6. **Return Results**
   Results (GeoJSON with optimal sites and cost data) are sent back to the frontend.

7. **Visualization**
   Recommended sites are rendered on the map with detailed cost breakdowns and infrastructure information.

---

## Real Optimization Methodology

### LCOH Calculation Formula

```
LCOH = (CAPEX + ∑ OPEX/(1+r)^t) / (∑ Production/(1+r)^t)

Where:
- CAPEX = Capital expenditure (solar, wind, electrolyzer, storage, grid)
- OPEX = Annual operational expenditure (O&M, labor, insurance, water)
- r = Discount rate (8%)
- t = Year (1-20 project lifetime)
- Production = Annual hydrogen production (kg)
```

### Cost Parameters

- **Solar CAPEX**: $1,200/kW
- **Wind CAPEX**: $1,400/kW
- **Electrolyzer CAPEX**: $800/kW
- **Storage CAPEX**: $200/kWh
- **Grid Connection**: $100/kW
- **O&M Factor**: 2.5% of CAPEX annually
- **Project Lifetime**: 20 years
- **Discount Rate**: 8%

### Optimization Factors

1. **Renewable Potential**: Solar irradiance (70%) + wind speed (30%) weighted average
2. **Infrastructure Proximity**: Distance-based bonuses/penalties for ports, industrial parks, substations
3. **Land Suitability**: Terrain and environmental factors
4. **Transportation Costs**: Pipeline and road network analysis
5. **Grid Connectivity**: Distance to electrical infrastructure

---

## Database Schema

### Tables

- **renewable_potential**: Solar irradiance, wind speed, land suitability, grid distance
- **infrastructure**: Ports, industrial parks, substations with capacity and status
- **transportation_network**: Roads, rail, pipelines with capacity and status
- **optimization_results**: Historical optimization results with full metadata

### Sample Data

- **6 Indian States**: Gujarat, Rajasthan, Maharashtra, Karnataka, Tamil Nadu, Andhra Pradesh
- **Real Coordinates**: Actual industrial locations (Bhuj Solar Park, Jamnagar Port, etc.)
- **Realistic Parameters**: Based on actual renewable potential and infrastructure data

---

## Quick Start - Running Locally

### Prerequisites

- Python 3.8+ and Node.js 18+ installed
- PostgreSQL 16+ with PostGIS extension
- Git for cloning the repository

### Setup Instructions

1. **Clone and navigate to the project:**

   ```bash
   git clone <repository-url>
   cd GreenH2
   ```

2. **Database Setup:**

   ```bash
   # Install PostgreSQL and PostGIS (Ubuntu/Debian)
   sudo apt install postgresql postgresql-contrib postgresql-16-postgis-3 postgresql-16-postgis-3-scripts

   # Create database and user
   sudo -u postgres createuser --superuser omman
   createdb greenh2_db

   # Set password
   sudo -u postgres psql -c "ALTER USER omman PASSWORD 'greenh2_password';"

   # Enable PostGIS extension
   psql -d greenh2_db -c "CREATE EXTENSION postgis;"

   # Run database setup script
   cd backend
   python setup_database.py
   ```

3. **Start the Backend (Terminal 1):**

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Start the Frontend (Terminal 2):**

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

5. **Access the Application:**
   - Frontend: `http://localhost:5173/`
   - Backend API: `http://localhost:8000/`
   - API Documentation: `http://localhost:8000/docs`

### Using the Application

1. **Select a region** from the dropdown (Gujarat, Rajasthan, Maharashtra, etc.)
2. **Adjust optimization parameters** (max LCOH, production capacity, etc.)
3. **Click "Run Optimization"** to find optimal hydrogen production sites
4. **View results** on the interactive map with detailed cost breakdowns
5. **Click on markers** to see detailed information including:
   - LCOH breakdown (production vs transport costs)
   - Infrastructure proximity
   - Renewable potential scores
   - Annual production capacity

---

## API Endpoints

### Core Endpoints

- **POST** `/optimize` - Run site optimization (with wrapper response)
- **POST** `/api/optimize` - Run site optimization (direct GeoJSON)
- **GET** `/optimizer/status` - Get optimization engine status
- **GET** `/health` - Health check
- **GET** `/` - API status

### Request Format

```json
{
  "region": "gujarat",
  "max_cost": 5.0,
  "min_production": 1000,
  "proximity_to_grid": true
}
```

### Response Format

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [longitude, latitude]
      },
      "properties": {
        "site_name": "Bhuj Solar Park",
        "lcoh": 3.5,
        "production_cost": 2.63,
        "transport_cost": 0.88,
        "rank": 1,
        "infrastructure_proximity_km": 45.2,
        "annual_production_tonnes": 1250.5
      }
    }
  ],
  "metadata": {
    "optimization_criteria": {...},
    "algorithm": "GEOH2_Real_Optimizer_v1.0",
    "data_sources": [...]
  }
}
```

---

## Development Features

### Real-Time Optimization

- **Database-driven**: Queries real geospatial data from PostGIS
- **Multi-criteria**: Considers renewable potential, infrastructure, costs
- **Scalable**: Can handle thousands of potential sites
- **Fallback**: Graceful degradation to simulation if database unavailable

### Indian States Support

- **Gujarat**: Bhuj Solar Park, Jamnagar Port, Vadodara Chemical
- **Rajasthan**: Jaisalmer Wind, Bikaner Solar, Jodhpur Industrial
- **Maharashtra**: Mumbai Port, Pune Technology, Dhule Solar
- **Karnataka**: Bengaluru Tech, Mangalore Port, Tumkur Solar
- **Tamil Nadu**: Chennai Port, Coimbatore Industrial, Tuticorin Port
- **Andhra Pradesh**: Visakhapatnam Port, Vijayawada Industrial, Tirupati Solar

### Cost Realism

- **Actual CAPEX values** based on current market rates
- **Regional variations** in renewable potential
- **Infrastructure bonuses** for proximity to existing facilities
- **Transportation costs** based on distance and infrastructure type

---

## Architecture

### Backend Architecture

```
FastAPI Server
├── main.py (API endpoints)
├── optimizer.py (optimization engine)
├── real_optimizer.py (GEOH2 computational core)
├── setup_database.py (database initialization)
└── requirements.txt (Python dependencies)
```

### Frontend Architecture

```
React Application
├── App.tsx (main application)
├── ControlPanel.tsx (optimization controls)
├── components/
│   ├── Map.tsx (map container)
│   └── MapView.tsx (map markers and results)
└── package.json (Node dependencies)
```

### Database Architecture

```
PostgreSQL + PostGIS
├── renewable_potential (solar, wind, land data)
├── infrastructure (ports, industrial parks)
├── transportation_network (roads, rail, pipelines)
└── optimization_results (historical results)
```

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with both database and simulation modes
5. Submit a pull request

### Development Setup

```bash
# Database setup
createdb greenh2_db
psql -d greenh2_db -c "CREATE EXTENSION postgis;"
python backend/setup_database.py

# Backend development
cd backend && pip install -r requirements.txt
uvicorn main:app --reload

# Frontend development
cd frontend && npm install
npm run dev
```

---

## License

This project is private and proprietary. All rights reserved.

---

## Support

For questions or issues:

1. Check the API documentation at `http://localhost:8000/docs`
2. Review the database logs for optimization details
3. Test with different regions and parameters
4. Check the fallback simulation if database issues occur

---

## Key Features

### 🌍 Interactive Map Interface

- A user-friendly, responsive map built with **Mapbox GL JS**.
- Users can pan, zoom, and query data by clicking on specific regions.

### 🗂️ Layered Data Visualization

Toggle multiple data layers on and off to gain a comprehensive geospatial understanding. Layers include:

- Existing/Planned Hydrogen Assets (Plants, Storage, Pipelines)
- Renewable Energy Potential (Solar Irradiance, Wind Speed)
- High-Capacity Grid Infrastructure
- Major Demand Centers (Industrial Hubs, Ports)
- Transport & Logistics Networks (Roads, Rail)

### ⚙️ Advanced Optimization Engine

- Powered by the **GEOH2 computational core**.
- Calculates the **Levelized Cost of Hydrogen (LCOH)** for thousands of potential sites.

### 📊 Scenario-Based Site Recommendations

- Define investment criteria (e.g., proximity to solar, distance to port, target production cost).
- Receive a ranked list of optimal project locations highlighted on the map.

### 📈 Dynamic Dashboards

- Clicking a recommended site reveals a dashboard with **D3.js charts** breaking down LCOH into production, storage, and transport costs.

---

## Tech Stack

- **Frontend:** React, Mapbox GL JS, D3.js, Tailwind CSS
- **Backend API:** Python (FastAPI)
- **Computational Engine:** Modified version of GEOH2 (Snakemake workflow, PyPSA)
- **Database:** PostGIS (efficient geospatial querying)

---

## How It Works

1. **User Interaction**  
   Define an area of interest and set criteria (e.g., _“Find the cheapest locations for a new plant in Gujarat close to the grid”_) via the web interface.

2. **API Request**  
   React frontend sends a structured request to the FastAPI backend.

3. **Optimization Trigger**  
   Backend validates the request and triggers the GEOH2 computational engine with the given parameters.

4. **Data Processing**  
   The engine fetches geospatial data from PostGIS, runs LCOH optimization, and calculates the best sites.

5. **Return Results**  
   Results (GeoJSON with optimal sites and cost data) are sent back to the frontend.

6. **Visualization**  
   Recommended sites are rendered on the map with dashboards showing detailed cost breakdowns.

---

## Quick Start - Running Locally

### Prerequisites

- Python 3.8+ and Node.js 18+ installed
- Git for cloning the repository

### Setup Instructions

1. **Clone and navigate to the project:**

   ```bash
   git clone <repository-url>
   cd GreenH2
   ```

2. **Start the Backend (Terminal 1):**

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Start the Frontend (Terminal 2):**

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the Application:**
   - Frontend: `http://localhost:5173/`
   - Backend API: `http://localhost:8000/`
   - API Documentation: `http://localhost:8000/docs`

### Using the Application

1. **Select a region** from the dropdown in the control panel
2. **Adjust optimization parameters** (max LCOH, production capacity, etc.)
3. **Click "Run Optimization"** to find optimal hydrogen production sites
4. **View results** on the interactive map with cost breakdowns
5. **Click on markers** to see detailed D3.js cost analysis charts

For detailed setup instructions and troubleshooting, see [RUN.md](./RUN.md).
