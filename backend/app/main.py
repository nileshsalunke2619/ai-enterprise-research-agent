from fastapi import FastAPI
from app.config import settings


app = FastAPI(
    title="AI Enterprise Research & Action Agent",
    description="Backend API for an AI-powered enterprise research agent.",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": f"{settings.app_name} API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "environment": settings.environment
    }