# GreenH2 Application - Run Instructions

This document provides comprehensive instructions for running both the backend (FastAPI) and frontend (React) applications with the real GEOH2 optimization engine.

## Prerequisites

- Python 3.8+ installed
- Node.js 18+ installed
- PostgreSQL 16+ with PostGIS extension
- npm or yarn package manager

## Database Setup

### 1. Install PostgreSQL and PostGIS

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib postgresql-16-postgis-3 postgresql-16-postgis-3-scripts
```

**macOS (with Homebrew):**

```bash
brew install postgresql
brew install postgis
```

**Windows:**
Download and install from: https://www.postgresql.org/download/windows/

### 2. Create Database and User

```bash
# Start PostgreSQL service
sudo systemctl start postgresql  # Linux
# or
brew services start postgresql   # macOS

# Create superuser (replace 'omman' with your username)
sudo -u postgres createuser --superuser omman

# Create database
createdb greenh2_db

# Set password for user
sudo -u postgres psql -c "ALTER USER omman PASSWORD 'greenh2_password';"

# Enable PostGIS extension
psql -d greenh2_db -c "CREATE EXTENSION postgis;"
```

### 3. Initialize Database Schema

```bash
cd backend
python setup_database.py
```

**Database Configuration:**

- **Host:** localhost
- **Port:** 5432
- **Database:** greenh2_db
- **Username:** omman
- **Password:** greenh2_password

## Backend Setup and Run

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Virtual Environment (if not already created)

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**On Linux/macOS:**

```bash
source venv/bin/activate
```

**On Windows:**

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required Packages:**

- fastapi
- uvicorn
- psycopg2-binary
- numpy
- pandas
- shapely
- geopandas
- rasterio
- scipy
- python-multipart

### 5. Run the FastAPI Server

**Option 1: Using uvicorn directly (recommended for development)**

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Option 2: Using the main.py file**

```bash
python main.py
```

### 6. Verify Backend is Running

- Open your browser and go to: `http://localhost:8000/`
- You should see: `{"status": "API is running"}`
- API documentation: `http://localhost:8000/docs`
- Optimizer status: `http://localhost:8000/optimizer/status`

## Frontend Setup and Run

### 1. Navigate to Frontend Directory

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Run the React Development Server

```bash
npm run dev
```

### 4. Verify Frontend is Running

- Open your browser and go to: `http://localhost:5173/`
- You should see the React application running

## Running Both Applications

### Terminal 1 - Backend

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2 - Frontend

```bash
cd frontend
npm run dev
```

## Quick Start Commands

### One-liner commands for quick setup:

**Database Setup:**

```bash
sudo -u postgres createuser --superuser omman
createdb greenh2_db
sudo -u postgres psql -c "ALTER USER omman PASSWORD 'greenh2_password';"
psql -d greenh2_db -c "CREATE EXTENSION postgis;"
cd backend && python setup_database.py
```

**Backend:**

```bash
cd backend && source venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**

```bash
cd frontend && npm run dev
```

### Verify Both Services Are Running:

1. **Backend API**: Visit `http://localhost:8000/` - Should show `{"status": "API is running"}`
2. **Frontend App**: Visit `http://localhost:5173/` - Should show the GreenH2 application
3. **API Documentation**: Visit `http://localhost:8000/docs` - Interactive API docs
4. **Database Connection**: Check optimizer status at `http://localhost:8000/optimizer/status`

## Available Endpoints

### Backend API Endpoints

- **Root**: `http://localhost:8000/` - API status
- **Health Check**: `http://localhost:8000/health` - Health status
- **Optimizer Status**: `http://localhost:8000/optimizer/status` - Optimization engine status
- **Site Optimization**: `POST http://localhost:8000/optimize` - Run site optimization (with wrapper)
- **API Optimization**: `POST http://localhost:8000/api/optimize` - Run site optimization (direct GeoJSON)
- **API Docs**: `http://localhost:8000/docs` - Interactive documentation
- **ReDoc**: `http://localhost:8000/redoc` - Alternative documentation

### Frontend

- **Application**: `http://localhost:5173/` - React application

## Optimization API Usage

### Running Site Optimization

The backend includes a **real GEOH2 computational engine** for site optimization with database-driven calculations. Two endpoints are available:

#### Option 1: `/optimize` (with wrapper)

**POST** `http://localhost:8000/optimize`

Returns a wrapped response with status and metadata.

#### Option 2: `/api/optimize` (direct GeoJSON)

**POST** `http://localhost:8000/api/optimize`

Returns the GeoJSON result directly from the optimization function.

**Request Body:**

```json
{
  "region": "gujarat",
  "max_cost": 5.0,
  "min_production": 1000,
  "proximity_to_grid": true
}
```

**Response:**
Returns GeoJSON with recommended sites including:

- Site coordinates (longitude, latitude)
- LCOH (Levelized Cost of Hydrogen)
- Production cost breakdown
- Transport cost breakdown
- Site ranking
- Infrastructure proximity
- Annual production capacity

### Example cURL Requests:

**Using `/optimize` (with wrapper):**

```bash
curl -X POST "http://localhost:8000/optimize" \
  -H "Content-Type: application/json" \
  -d '{"region": "gujarat", "max_cost": 5.0}'
```

**Using `/api/optimize` (direct GeoJSON):**

```bash
curl -X POST "http://localhost:8000/api/optimize" \
  -H "Content-Type: application/json" \
  -d '{"region": "gujarat", "max_cost": 4.5}'
```

## Database Schema Details

### Tables Created by setup_database.py

1. **renewable_potential**

   - id (SERIAL PRIMARY KEY)
   - state (VARCHAR)
   - site_name (VARCHAR)
   - latitude (FLOAT)
   - longitude (FLOAT)
   - solar_irradiance (FLOAT) - kWh/m²/day
   - wind_speed (FLOAT) - m/s
   - land_suitability (FLOAT) - 0-1 scale
   - grid_distance_km (FLOAT)
   - geom (GEOMETRY(Point, 4326))

2. **infrastructure**

   - id (SERIAL PRIMARY KEY)
   - state (VARCHAR)
   - facility_name (VARCHAR)
   - facility_type (VARCHAR) - 'port', 'industrial_park', 'substation'
   - latitude (FLOAT)
   - longitude (FLOAT)
   - capacity_mw (FLOAT)
   - status (VARCHAR) - 'operational', 'planned', 'under_construction'
   - geom (GEOMETRY(Point, 4326))

3. **transportation_network**

   - id (SERIAL PRIMARY KEY)
   - state (VARCHAR)
   - network_name (VARCHAR)
   - network_type (VARCHAR) - 'road', 'rail', 'pipeline'
   - latitude (FLOAT)
   - longitude (FLOAT)
   - capacity_tonnes_year (FLOAT)
   - status (VARCHAR)
   - geom (GEOMETRY(Point, 4326))

4. **optimization_results**
   - id (SERIAL PRIMARY KEY)
   - region (VARCHAR)
   - criteria (JSONB)
   - results (JSONB)
   - created_at (TIMESTAMP)

### Sample Data Included

**States with Real Locations:**

- **Gujarat**: Bhuj Solar Park, Jamnagar Port, Vadodara Chemical Hub
- **Rajasthan**: Jaisalmer Wind Farm, Bikaner Solar Park, Jodhpur Industrial Area
- **Maharashtra**: Mumbai Port, Pune Technology Park, Dhule Solar Park
- **Karnataka**: Bengaluru Tech Hub, Mangalore Port, Tumkur Solar Park
- **Tamil Nadu**: Chennai Port, Coimbatore Industrial, Tuticorin Port
- **Andhra Pradesh**: Visakhapatnam Port, Vijayawada Industrial, Tirupati Solar Park

## Optimization Engine Details

### Real GEOH2 Computational Core

The optimization engine uses:

1. **Database Queries**: Fetches real geospatial data from PostGIS
2. **LCOH Calculations**: Industry-standard formulas with real cost parameters
3. **Multi-Criteria Analysis**: Renewable potential, infrastructure proximity, costs
4. **Geospatial Analysis**: Haversine distance calculations, spatial joins
5. **Cost Optimization**: Production costs, transport costs, infrastructure bonuses

### Cost Parameters

- **Solar CAPEX**: $1,200/kW
- **Wind CAPEX**: $1,400/kW
- **Electrolyzer CAPEX**: $800/kW
- **Storage CAPEX**: $200/kWh
- **Grid Connection**: $100/kW
- **O&M Factor**: 2.5% of CAPEX annually
- **Project Lifetime**: 20 years
- **Discount Rate**: 8%

### Optimization Algorithm

1. **Data Retrieval**: Query renewable potential and infrastructure data
2. **Potential Scoring**: Calculate renewable energy potential (70% solar + 30% wind)
3. **Infrastructure Analysis**: Calculate proximity bonuses/penalties
4. **LCOH Calculation**: Compute levelized cost using industry formulas
5. **Ranking**: Sort sites by LCOH and apply multi-criteria filters
6. **GeoJSON Generation**: Format results for map visualization

## Development Workflow

1. **Start Database**: Ensure PostgreSQL is running with PostGIS
2. **Initialize Schema**: Run `python setup_database.py` if needed
3. **Start Backend First**: Always start the FastAPI server before the frontend
4. **Hot Reload**: Both servers support hot reloading for development
5. **CORS**: Backend is configured to accept requests from the frontend
6. **API Calls**: Frontend can make API calls to `http://localhost:8000`

## Troubleshooting

### Database Issues

- **Connection Failed**: Check if PostgreSQL is running: `sudo systemctl status postgresql`
- **User Not Found**: Create user: `sudo -u postgres createuser --superuser omman`
- **Password Issues**: Set password: `sudo -u postgres psql -c "ALTER USER omman PASSWORD 'greenh2_password';"`
- **PostGIS Missing**: Enable extension: `psql -d greenh2_db -c "CREATE EXTENSION postgis;"`
- **Permission Denied**: Grant permissions: `sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE greenh2_db TO omman;"`

### Backend Issues

- **Port already in use**: Change port with `--port 8001`
- **Virtual environment not activated**: Make sure you see `(venv)` in your terminal
- **Dependencies missing**: Run `pip install -r requirements.txt`
- **Database connection error**: Check database credentials and PostGIS extension
- **Import errors**: Install missing packages: `pip install psycopg2-binary numpy pandas shapely`

### Frontend Issues

- **Port already in use**: Vite will automatically use the next available port
- **Dependencies missing**: Run `npm install`
- **Node version**: Ensure you have Node.js 18+ installed
- **API connection failed**: Check if backend is running on port 8000

### Optimization Issues

- **No results returned**: Check database has sample data
- **Database unavailable**: System falls back to simulation mode
- **Invalid region**: Use supported regions: gujarat, rajasthan, maharashtra, karnataka, tamil_nadu, andhra_pradesh
- **High LCOH values**: Check cost parameters and renewable potential data

## Environment Variables

Create `.env` files in respective directories for environment-specific configuration:

### Backend (.env)

```
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=greenh2_db
DATABASE_USER=omman
DATABASE_PASSWORD=greenh2_password
SECRET_KEY=your_secret_key_here
DEBUG=True
```

### Frontend (.env)

```
VITE_API_URL=http://localhost:8000
VITE_MAPBOX_TOKEN=your_mapbox_token_here
```

## Production Deployment

For production deployment, additional configuration will be needed:

- Environment variables for production database
- Database connection pooling
- Static file serving for frontend
- Security headers and CORS configuration
- Production build for frontend: `npm run build`
- Reverse proxy (nginx) for serving both frontend and backend
- SSL/TLS certificates
- Database backup and recovery procedures

## Testing the System

### 1. Test Database Connection

```bash
cd backend
python -c "import psycopg2; conn = psycopg2.connect('dbname=greenh2_db user=omman password=greenh2_password'); print('Database connected successfully')"
```

### 2. Test Optimization API

```bash
curl -X POST "http://localhost:8000/api/optimize" \
  -H "Content-Type: application/json" \
  -d '{"region": "gujarat", "max_cost": 5.0}'
```

### 3. Test Frontend Integration

1. Open `http://localhost:5173/`
2. Select "Gujarat" from region dropdown
3. Click "Run Optimization"
4. Verify markers appear on map with cost information

## Performance Optimization

### Database Performance

- Spatial indexes on geometry columns
- Query optimization for geospatial operations
- Connection pooling for production

### API Performance

- Asynchronous processing for optimization requests
- Caching for frequently accessed data
- Pagination for large result sets

### Frontend Performance

- Lazy loading of map components
- Optimized bundle size with code splitting
- Efficient state management

## Monitoring and Logging

### Backend Logs

- FastAPI automatically logs requests and responses
- Database connection logs
- Optimization processing logs

### Database Monitoring

- Query performance monitoring
- Connection pool status
- Table size and index usage

### Frontend Monitoring

- Network request monitoring
- Error boundary components
- Performance metrics

## Backup and Recovery

### Database Backup

```bash
pg_dump greenh2_db > greenh2_backup.sql
```

### Database Restore

```bash
psql greenh2_db < greenh2_backup.sql
```

### Code Backup

- Use Git for version control
- Regular commits and pushes to repository
- Tag releases for production deployments

## Support and Maintenance

### Regular Maintenance Tasks

1. **Database**: Vacuum and analyze tables monthly
2. **Dependencies**: Update Python and Node packages regularly
3. **Security**: Monitor for security updates and patches
4. **Performance**: Monitor query performance and optimize slow queries

### Getting Help

1. Check API documentation at `http://localhost:8000/docs`
2. Review application logs for error messages
3. Test with different regions and parameters
4. Check database connectivity and data integrity
5. Verify all services are running and accessible

### Common Issues and Solutions

- **Database connection timeout**: Increase connection timeout in application settings
- **Memory issues**: Monitor memory usage and optimize queries
- **Slow optimization**: Add database indexes and optimize geospatial queries
- **Frontend loading issues**: Check network connectivity and API availability
