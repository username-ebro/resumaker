#!/usr/bin/env python3
"""Run database migration to add resume_structure column"""

import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv("backend/.env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SECRET_KEY")

# Create admin client
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Migration SQL
migration_sql = """
-- Add resume_structure column to resume_versions table
ALTER TABLE resume_versions
ADD COLUMN IF NOT EXISTS resume_structure JSONB;

-- Update existing records to use content as resume_structure if needed
UPDATE resume_versions
SET resume_structure = content
WHERE resume_structure IS NULL;
"""

try:
    # Execute migration
    print("Running migration to add resume_structure column...")

    # Split into individual statements
    statements = [s.strip() for s in migration_sql.split(';') if s.strip()]

    for statement in statements:
        print(f"\nExecuting: {statement[:50]}...")
        result = supabase.rpc('exec_sql', {'query': statement}).execute()
        print(f"✅ Success")

    print("\n✅ Migration completed successfully!")

except Exception as e:
    print(f"\n❌ Migration failed: {e}")
    print("\nTrying alternative approach using direct table modification...")

    try:
        # Try using the Supabase client's table operations
        # First, check if column exists by trying to select it
        test = supabase.table("resume_versions").select("resume_structure").limit(1).execute()
        print("✅ Column already exists!")
    except Exception as check_error:
        print(f"Column doesn't exist yet: {check_error}")
        print("\n⚠️ Manual migration needed. Please run this SQL in Supabase SQL Editor:")
        print("\n" + migration_sql)
