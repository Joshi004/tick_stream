from fastapi import FastAPI, Depends
import time
from datetime import datetime
from app.core.config import settings
from app.db.session import get_db
from app.api.endpoints import router as api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "service": settings.PROJECT_NAME
    }

@app.get("/db-test")
async def db_test(db=Depends(get_db)):
    """Test database connectivity"""
    start_time = time.time()
    # Run a simple query to check if the database is up and connected
    from sqlalchemy import text
    result = db.execute(text("SELECT 1 as is_alive")).fetchone()
    end_time = time.time()
    
    return {
        "status": "ok" if result.is_alive == 1 else "error",
        "response_time_ms": round((end_time - start_time) * 1000, 2),
        "timestamp": datetime.utcnow().isoformat()
    }
