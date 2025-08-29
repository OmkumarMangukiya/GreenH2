# GreenH2 

An interactive, data-driven platform for optimizing green hydrogen infrastructure investments.

**GreenH2** is a full-stack web application designed to solve the critical challenge of strategic infrastructure placement. It provides urban planners, energy companies, and policy analysts with an intuitive, map-based tool to identify the most cost-effective and high-impact locations for new green hydrogen projects.

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
   Define an area of interest and set criteria (e.g., *“Find the cheapest locations for a new plant in Gujarat close to the grid”*) via the web interface.  

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
