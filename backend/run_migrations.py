#!/usr/bin/env python3
"""
Run database migrations against Supabase
"""

import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# Database connection (URL-encoded password)
DATABASE_URL = os.getenv("DATABASE_URL")

def run_migrations():
    """Execute all migration files in order"""

    migration_files = [
        "migrations/001_enums.sql",
        "migrations/002_core_tables.sql",
        "migrations/003_import_reference_tables.sql",
        "migrations/004_resume_ats_tables.sql",
        "migrations/005_utility_tables.sql"
    ]

    try:
        # Connect to database
        print(f"Connecting to database...")
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = False
        cursor = conn.cursor()

        for migration_file in migration_files:
            print(f"\n📝 Running {migration_file}...")

            with open(migration_file, 'r') as f:
                sql = f.read()

            try:
                cursor.execute(sql)
                conn.commit()
                print(f"✅ {migration_file} completed successfully")
            except Exception as e:
                print(f"❌ Error in {migration_file}: {e}")
                conn.rollback()
                raise

        # Verify tables created
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)

        tables = cursor.fetchall()
        print(f"\n✅ Migration complete! Created {len(tables)} tables:")
        for table in tables:
            print(f"   - {table[0]}")

        cursor.close()
        conn.close()

        print("\n🎉 All migrations completed successfully!")

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        raise

if __name__ == "__main__":
    run_migrations()
