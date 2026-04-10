# =============================================================================
# STUDENT RECORDS MANAGEMENT SYSTEM
# File: database/setup_database.py
# Purpose: Executes schema.sql against Azure PostgreSQL to create all tables.
# =============================================================================

import psycopg2
from dotenv import load_dotenv
import os

# -----------------------------------------------------------------------------
# Load environment variables from .env file
# -----------------------------------------------------------------------------
load_dotenv()

# -----------------------------------------------------------------------------
# Read database credentials from environment variables
# -----------------------------------------------------------------------------
DB_HOST     = os.getenv('DB_HOST')
DB_NAME     = os.getenv('DB_NAME')
DB_USER     = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT     = os.getenv('DB_PORT', '5432')

# -----------------------------------------------------------------------------
# Read the schema.sql file
# -----------------------------------------------------------------------------
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')


def setup_database():
    """
    Connects to Azure PostgreSQL and executes the schema.sql file
    to create all tables if they do not already exist.
    """
    connection = None

    try:
        # Establish connection
        print("Connecting to Azure PostgreSQL...")
        connection = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cursor = connection.cursor()
        print("Connection successful.")

        # Read schema.sql file
        print("Reading schema.sql...")
        with open(SCHEMA_PATH, 'r') as schema_file:
            sql = schema_file.read()
        print("Schema file loaded successfully.")

        # Execute the schema
        print("Creating tables...")
        cursor.execute(sql)
        connection.commit()
        print("All tables created successfully.")

        # Confirm tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print("\nTables now present in database:")
        for table in tables:
            print(f"  - {table[0]}")

    except Exception as e:
        print(f"\nError: {e}")
        if connection:
            connection.rollback()

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("\nDatabase connection closed.")


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    setup_database()