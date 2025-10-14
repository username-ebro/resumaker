"""Database connection and client setup"""

from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")  # For auth
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SECRET_KEY")  # For database

# Auth client (for signup/login)
supabase_auth: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Admin client (for database operations, bypasses RLS)
supabase_admin: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def get_supabase() -> Client:
    """Get Supabase admin client (bypasses RLS)"""
    return supabase_admin

def get_supabase_auth() -> Client:
    """Get Supabase auth client (for auth operations)"""
    return supabase_auth
