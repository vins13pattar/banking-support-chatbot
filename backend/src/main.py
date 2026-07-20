"""FastAPI Application Entrypoint."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.api.routes import router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events."""
    logger.info("Starting Banking Support Chatbot API...")
    # Optional: ensure DB is created (though Alembic handles this)
    yield
    logger.info("Shutting down API...")


app = FastAPI(
    title="Banking Support Chatbot API",
    description="Custom backend for admin dashboard and HITL workflows",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.main:app", 
        host=settings.api_host, 
        port=settings.api_port, 
        reload=True
    )
