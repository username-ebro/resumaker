"""
Resumaker Backend - FastAPI Application
Main entry point for the API server
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from dotenv import load_dotenv
from datetime import datetime
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os

# Import routers
from app.routers import auth, upload, imports, conversation, references, resumes, jobs, knowledge

# Import logging configuration
from app.logging_config import setup_logging

# Load environment variables
load_dotenv()

# Initialize logging
logger = setup_logging()

# ============================================================================
# ENVIRONMENT VALIDATION - RUN BEFORE ANYTHING ELSE
# ============================================================================
REQUIRED_ENV_VARS = [
    "SUPABASE_URL",
    "SUPABASE_ANON_KEY",
    "SUPABASE_SECRET_KEY",
    "CLAUDE_API_KEY",
    "GEMINI_API_KEY",
]

missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]

if missing_vars:
    error_msg = f"""
{'=' * 70}
STARTUP ERROR: Missing Required Environment Variables
{'=' * 70}

The following environment variables are required but not set:

{chr(10).join(f'  ❌ {var}' for var in missing_vars)}

Please set these variables in:
  - Railway: Project Settings → Variables
  - Local: backend/.env file

{'=' * 70}
"""
    logger.error(error_msg)
    raise ValueError(f"Missing required environment variables: {missing_vars}")

logger.info("✅ All required environment variables are set")
# ============================================================================

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

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

# Attach limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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
    allowed_hosts=["resumaker-backend-production.up.railway.app", "localhost", "127.0.0.1"]
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
    logger.info("Starting Resumaker API server")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
