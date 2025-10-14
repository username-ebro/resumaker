#!/usr/bin/env python3
"""Run database migrations: critical bug fix + resume management"""

import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv("backend/.env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SECRET_KEY")

# Create admin client
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Migration 1: Critical bug fix - auto_flagged column
migration_1_sql = """
-- Critical Bug Fix: Add auto_flagged column to truth_check_flags
ALTER TABLE truth_check_flags
ADD COLUMN IF NOT EXISTS auto_flagged BOOLEAN DEFAULT FALSE;

CREATE INDEX IF NOT EXISTS idx_truth_flags_auto
ON truth_check_flags(auto_flagged)
WHERE auto_flagged = TRUE;
"""

# Migration 2: Resume management features
migration_2_sql = """
-- Add star and archive columns to resume_versions
ALTER TABLE resume_versions
ADD COLUMN IF NOT EXISTS is_starred BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS is_archived BOOLEAN DEFAULT FALSE;

CREATE INDEX IF NOT EXISTS idx_resume_versions_starred ON resume_versions(is_starred);
CREATE INDEX IF NOT EXISTS idx_resume_versions_archived ON resume_versions(is_archived);

UPDATE resume_versions
SET is_starred = FALSE, is_archived = FALSE
WHERE is_starred IS NULL OR is_archived IS NULL;
"""

try:
    # Execute migration 1
    print("🔧 Running Migration 1: Critical bug fix (auto_flagged column)...")
    result = supabase.rpc('exec_sql', {'query': migration_1_sql}).execute()
    print("✅ Migration 1 complete - Added auto_flagged column to truth_check_flags")

    # Execute migration 2
    print("\n🔧 Running Migration 2: Resume management (star/archive columns)...")
    result = supabase.rpc('exec_sql', {'query': migration_2_sql}).execute()
    print("✅ Migration 2 complete - Added is_starred and is_archived columns")

    print("\n🎉 All migrations completed successfully!")

except Exception as e:
    print(f"\n❌ Migration failed: {e}")
    print("\nTrying alternative approach...")

    try:
        # Check if columns exist
        test1 = supabase.table("truth_check_flags").select("auto_flagged").limit(1).execute()
        print("✅ auto_flagged column already exists!")

        test2 = supabase.table("resume_versions").select("is_starred,is_archived").limit(1).execute()
        print("✅ is_starred and is_archived columns already exist!")

        print("\n✅ All columns present - migrations may have already been run")
    except Exception as check_error:
        print(f"Columns don't exist yet: {check_error}")
        print("\n⚠️ Manual migration needed. Please run this SQL in Supabase SQL Editor:")
        print("\n-- Migration 1 (Critical):")
        print(migration_1_sql)
        print("\n-- Migration 2 (Resume Management):")
        print(migration_2_sql)
