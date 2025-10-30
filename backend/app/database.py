"""Database connection and client setup"""

from supabase import create_client, Client
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv
import logging
import os

load_dotenv()

logger = logging.getLogger(__name__)

# Detect environment
IS_PRODUCTION = os.getenv("RAILWAY_ENVIRONMENT_NAME") is not None

# Validate required environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")  # For auth
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SECRET_KEY")  # For database

# Use connection pooler in production (Railway) to prevent connection exhaustion
# Pooler uses port 6543 with pgbouncer for connection pooling
if IS_PRODUCTION:
    SUPABASE_POOLER_URL = os.getenv("SUPABASE_POOLER_URL")
    if SUPABASE_POOLER_URL:
        logger.info("Using Supabase connection pooler for production")
        SUPABASE_URL = SUPABASE_POOLER_URL
    else:
        logger.warning("SUPABASE_POOLER_URL not set, using direct connection (may hit limits)")

required_vars = {
    "SUPABASE_URL": SUPABASE_URL,
    "SUPABASE_ANON_KEY": SUPABASE_ANON_KEY,
    "SUPABASE_SECRET_KEY": SUPABASE_SERVICE_KEY
}

missing = [var for var, value in required_vars.items() if not value]
if missing:
    raise ValueError(f"Missing required environment variables: {missing}")

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def create_supabase_client(url: str, key: str, client_type: str) -> Client:
    """Create Supabase client with connection validation and retry logic"""
    try:
        client = create_client(url, key)
        # Validate connection with simple query
        client.table("user_profiles").select("id").limit(1).execute()
        logger.info(f"Supabase {client_type} connection established")
        return client
    except Exception as e:
        logger.error(f"Failed to connect to Supabase ({client_type}): {e}")
        raise

# Auth client (for signup/login)
supabase_auth: Client = create_supabase_client(SUPABASE_URL, SUPABASE_ANON_KEY, "auth")

# Admin client (for database operations, bypasses RLS)
supabase_admin: Client = create_supabase_client(SUPABASE_URL, SUPABASE_SERVICE_KEY, "admin")

def get_supabase() -> Client:
    """Get Supabase admin client (bypasses RLS)"""
    return supabase_admin

def get_supabase_auth() -> Client:
    """Get Supabase auth client (for auth operations)"""
    return supabase_auth
