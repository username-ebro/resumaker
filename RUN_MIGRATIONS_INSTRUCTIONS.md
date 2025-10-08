# Running Database Migrations

## Quick Instructions

1. Go to Supabase Dashboard: https://supabase.com/dashboard/project/nkfrqysxrwfqqzpsjtlh
2. Click "SQL Editor" in left sidebar
3. Click "New Query"
4. Copy and paste the content from `backend/migrations/full_migration.sql`
5. Click "Run" or press Cmd+Enter

## What This Does

Creates 14 tables:
- user_profiles
- user_knowledge_base
- conversations
- user_data_points
- conversation_imports
- resume_artifacts
- reference_requests
- reference_responses
- ats_systems (with seed data)
- job_postings
- resume_versions
- truth_check_flags
- user_translations
- activity_log

Plus 8 ENUM types and all RLS policies.

## Verify Success

After running, you should see:
- 14 tables in the "Table Editor"
- 8 custom types in "Database" → "Types"

## Alternative: Run via CLI

If you prefer command line:

```bash
cd backend
cat migrations/full_migration.sql | psql "postgresql://postgres:mpx4FZN6rnv%40djz%21pvq@db.nkfrqysxrwfqqzpsjtlh.supabase.co:5432/postgres"
```

Note: Password is URL-encoded (@ = %40, ! = %21)
