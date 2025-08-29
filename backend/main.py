from fastapi import FastAPI, HTTPException                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
from optimizer import run_optimization, get_optimization_status

# Create FastAPI app instance
app = FastAPI(
    title="GreenH2 API",
    description="API for GreenH2 application",
    version="1.0.0"
)
                                                                                                                                                                                                                            
# Add CORS middleware to allow all origins during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def root():
    """Root endpoint that returns API status"""
    return {"status": "API is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "GreenH2 API is operational"}

# Pydantic model for optimization criteria
class OptimizationCriteria(BaseModel):
    region: str
    max_cost: float = 6.0
    min_production: int = 1000
    proximity_to_grid: bool = True
    additional_criteria: Dict[str, Any] = {}

@app.post("/optimize")
async def optimize_sites(criteria: OptimizationCriteria):
    """
    Run site optimization using the GEOH2 computational engine
    """
    try:
        # Convert Pydantic model to dict
        criteria_dict = criteria.dict()
        
        # Run optimization
        result = run_optimization(criteria_dict)
        
        return {
            "status": "success",
            "message": "Optimization completed successfully",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")

@app.post("/api/optimize")
async def api_optimize_sites(criteria: OptimizationCriteria):
    """
    API endpoint for site optimization using the GEOH2 computational engine
    Returns the GeoJSON result directly from the optimization function
    """
    try:
        # Convert Pydantic model to dict
        criteria_dict = criteria.dict()
        
        # Run optimization and return the GeoJSON result directly
        result = run_optimization(criteria_dict)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")

@app.get("/optimizer/status")
async def get_optimizer_status():
    """
    Get the status of the optimization engine
    """
    return get_optimization_status()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
