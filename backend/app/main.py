from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.api import merchant, campaign
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources on startup and clean up on shutdown."""
    init_db()
    yield


# Initialize FastAPI app
app = FastAPI(
    title="MerchantAI API",
    description="AI-powered merchant onboarding and campaign planning API",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(merchant.router)
app.include_router(campaign.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "MerchantAI API",
        "version": "1.0.0",
        "status": "running",
        "ai_provider": settings.ai_provider
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
