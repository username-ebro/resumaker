"""
Resumaker Backend - FastAPI Application
Main entry point for the API server
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from dotenv import load_dotenv
from datetime import datetime
import os

# Import routers
from app.routers import auth, upload, imports, conversation, references, resumes, jobs, knowledge

# Load environment variables
load_dotenv()

# Security Headers Middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        return response

# Initialize FastAPI app
app = FastAPI(
    title="Resumaker API",
    description="AI-powered resume builder with truth verification",
    version="1.0.0"
)

# Get CORS origins from environment variable
ALLOWED_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,http://localhost:3001"
).split(",")

# CORS Configuration - MUST BE BEFORE ROUTES
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=3600,
)

# Security Headers Middleware
app.add_middleware(SecurityHeadersMiddleware)

# Trusted Host Middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["resumaker.up.railway.app", "localhost", "127.0.0.1"]
)

# GZip Compression Middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include routers
app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(imports.router)
app.include_router(conversation.router)
app.include_router(references.router)
app.include_router(resumes.router)
app.include_router(jobs.router)
app.include_router(knowledge.router)

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
    """Detailed health check with database validation"""
    from app.database import supabase_admin

    status = {"status": "healthy", "checks": {}, "timestamp": datetime.utcnow().isoformat()}

    # Database check
    try:
        supabase_admin.table("user_profiles").select("id").limit(1).execute()
        status["checks"]["database"] = "connected"
    except Exception as e:
        status["checks"]["database"] = f"error: {str(e)}"
        status["status"] = "unhealthy"

    # API keys check
    status["checks"]["claude_api"] = "configured" if os.getenv("CLAUDE_API_KEY") else "missing"
    status["checks"]["gemini_api"] = "configured" if os.getenv("GEMINI_API_KEY") else "missing"

    return status

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
