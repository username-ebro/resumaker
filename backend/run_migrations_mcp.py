#!/usr/bin/env python3
"""
Run database migrations using Supabase Python client
"""

from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY")

def run_migrations():
    """Execute migrations using Supabase client"""

    migration_files = [
        "migrations/001_enums.sql",
        "migrations/002_core_tables.sql",
        "migrations/003_import_reference_tables.sql",
        "migrations/004_resume_ats_tables.sql",
        "migrations/005_utility_tables.sql"
    ]

    try:
        print("Connecting to Supabase...")
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

        for migration_file in migration_files:
            print(f"\n📝 Running {migration_file}...")

            with open(migration_file, 'r') as f:
                sql = f.read()

            try:
                # Use RPC to execute raw SQL
                result = supabase.rpc('exec_sql', {'sql_query': sql}).execute()
                print(f"✅ {migration_file} completed")
            except Exception as e:
                print(f"⚠️  Note: Direct SQL execution requires custom RPC function")
                print(f"   We'll use Supabase dashboard to run migrations manually")
                print(f"   Or use psql command line")
                break

        print("\n📌 Migration files created - ready to run via Supabase dashboard")
        print(f"   Location: backend/migrations/")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_migrations()
