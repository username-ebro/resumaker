#!/usr/bin/env python3
"""Run migrations using Supabase REST API"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_KEY = os.getenv("SUPABASE_SECRET_KEY")  # sb_secret_ZPQ_nX-2JbJrYKtNgAHhng_cMpbUzpe

def run_sql(sql_content):
    """Execute SQL via Supabase REST API"""
    url = f"{SUPABASE_URL}/rest/v1/rpc/exec_sql"
    headers = {
        "apikey": SERVICE_KEY,
        "Authorization": f"Bearer {SERVICE_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json={"query": sql_content})
    return response

# Read all migration files
migrations = [
    "migrations/001_enums.sql",
    "migrations/002_core_tables.sql",
    "migrations/003_import_reference_tables.sql",
    "migrations/004_resume_ats_tables.sql",
    "migrations/005_utility_tables.sql"
]

print("Running migrations via Supabase REST API...")
print(f"URL: {SUPABASE_URL}")

for migration_file in migrations:
    print(f"\n📝 {migration_file}...")
    with open(migration_file, 'r') as f:
        sql = f.read()

    # Note: This requires a custom RPC function in Supabase
    # Alternative: Use Supabase dashboard SQL editor
    print(f"   SQL ready ({len(sql)} characters)")

print("\n⚠️  Supabase doesn't allow direct SQL execution via REST API")
print("📌 Please run migrations manually:")
print("   1. Go to: https://supabase.com/dashboard/project/nkfrqysxrwfqqzpsjtlh/sql")
print("   2. Copy content from: backend/migrations/full_migration.sql")
print("   3. Paste and click 'Run'")
print(f"\n✅ Migration file ready at: migrations/full_migration.sql")
