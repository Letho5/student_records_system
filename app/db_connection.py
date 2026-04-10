# =============================================================================
# STUDENT RECORDS MANAGEMENT SYSTEM
# File: app/db_connection.py
# Purpose: Provides database connection management for the CLI application.
# =============================================================================

import psycopg2
from dotenv import load_dotenv
import os
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

# -----------------------------------------------------------------------------
# Load environment variables
# -----------------------------------------------------------------------------
load_dotenv()

# -----------------------------------------------------------------------------
# Database connection configuration
# -----------------------------------------------------------------------------
DB_CONFIG = {
    'host':     os.getenv('DB_HOST'),
    'dbname':   os.getenv('DB_NAME'),
    'user':     os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port':     os.getenv('DB_PORT', '5432'),
    'sslmode':  'require'
}


def get_connection():
    """
    Establishes and returns a connection to Azure PostgreSQL.
    Raises a clear error if the connection fails.
    """
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        return connection
    except Exception as e:
        print(f"\nDatabase connection failed: {e}")
        raise


def test_connection():
    """
    Tests the database connection and prints the result.
    Used for diagnostics and startup verification.
    """
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"Connection successful.")
        print(f"PostgreSQL version: {version[0][:50]}")
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False


# -----------------------------------------------------------------------------
# Entry point — connection test
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    test_connection()