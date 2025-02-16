import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_test_database():
    """Create test database if it doesn't exist."""
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="postgres",
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'test_db'"
        )
        exists = cursor.fetchone()
        
        if not exists:
            # Create database
            cursor.execute('CREATE DATABASE test_db')
            print("Created test database")
        else:
            print("Test database already exists")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error creating test database: {e}")
        raise

if __name__ == "__main__":
    create_test_database() 