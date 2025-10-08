"""
Resumaker Backend - FastAPI Application
Main entry point for the API server
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Import routers
from app.routers import auth, upload, imports, conversation, references, resumes, jobs

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Resumaker API",
    description="AI-powered resume builder with truth verification",
    version="1.0.0"
)

# CORS Configuration - MUST BE BEFORE ROUTES
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://resumaker.vercel.app",  # Production frontend
        "https://*.vercel.app"  # Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(imports.router)
app.include_router(conversation.router)
app.include_router(references.router)
app.include_router(resumes.router)
app.include_router(jobs.router)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Resumaker API is running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",  # TODO: Add actual DB check
        "services": {
            "claude": "available" if os.getenv("CLAUDE_API_KEY") else "missing_key",
            "gemini": "available" if os.getenv("GEMINI_API_KEY") else "missing_key",
            "supabase": "available" if os.getenv("SUPABASE_URL") else "missing_key"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
