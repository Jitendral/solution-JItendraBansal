import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is not set. Check your environment variables!")

def get_db_connection():
    """Establish a connection to PostgreSQL."""
    try:
        return psycopg2.connect(DATABASE_URL)
    except psycopg2.OperationalError as e:
        raise RuntimeError(f"❌ Database connection failed: {e}")
