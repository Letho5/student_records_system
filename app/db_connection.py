import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT'),
        sslmode='require'
    )
    return conn

# Test connection
if __name__ == "__main__":
    try:
        conn = get_connection()
        print(" Connected to database successfully!")
        conn.close()
    except Exception as e:
        print(f" Connection failed: {e}")