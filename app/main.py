"""FastAPI application for AAU Helpdesk Chatbot."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AAU Helpdesk Chatbot API",
    description="NLP-based chatbot for Addis Ababa University helpdesk services",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with system information."""
    try:
        # Check if models are loaded (will be implemented later)
        models_status = {
            "intent_model": "not_loaded",  # Will be updated when models are implemented
            "ner_model": "not_loaded",
            "vectorizer": "not_loaded"
        }
        
        return {
            "status": "healthy",
            "models": models_status,
            "api_version": "0.1.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": "unhealthy", "error": str(e)}
        )


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AAU Helpdesk Chatbot API",
        "version": "0.1.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD
    )
