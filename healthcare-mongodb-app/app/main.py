"""
Main FastAPI application
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from loguru import logger
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database
from app.config.database import db_instance

# Import routers
from app.routes import user_routes, sensor_data_routes, health_metrics_routes, prediction_routes, chat_routes

# Configure logger
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=os.getenv("LOG_LEVEL", "INFO")
)
logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="7 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
)
logger.add(
    "logs/error.log",
    rotation="10 MB",
    retention="30 days",
    level="ERROR",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("🚀 Starting Healthcare API...")
    await db_instance.connect()
    logger.info("✅ Application ready")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Healthcare API...")
    await db_instance.disconnect()
    logger.info("✅ Shutdown complete")

# Create FastAPI app
app = FastAPI(
    title="Healthcare Wearable API",
    description="API for managing healthcare wearable data, including sensor readings, health metrics, predictions, and AI coaching",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGIN", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"{request.method} {request.url.path} - Status: {response.status_code}")
    return response

# Health check endpoints
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "connected" if db_instance.is_connected() else "disconnected"
    }

@app.get("/api/health/database", tags=["Health"])
async def database_health():
    """Database health check with stats"""
    if not db_instance.is_connected():
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "message": "Database not connected"}
        )
    
    stats = await db_instance.get_stats()
    return {
        "status": "healthy",
        "database": stats
    }

# Include routers
app.include_router(user_routes.router, prefix="/api", tags=["Users"])
app.include_router(sensor_data_routes.router, prefix="/api", tags=["Sensor Data"])
app.include_router(health_metrics_routes.router, prefix="/api", tags=["Health Metrics"])
app.include_router(prediction_routes.router, prefix="/api", tags=["Predictions & Notifications"])
app.include_router(chat_routes.router, prefix="/api", tags=["AI Coach"])

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc) if os.getenv("NODE_ENV") == "development" else "An unexpected error occurred"
        }
    )

# 404 handler
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": f"Route {request.url.path} not found"
        }
    )

from datetime import datetime

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=os.getenv("NODE_ENV") == "development"
    )
