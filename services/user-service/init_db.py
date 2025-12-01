import psycopg2
import os
import time

def init_database():
    """Initialize the database"""
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'postgres')
    db_host = os.getenv('DB_HOST', 'postgres-db')
    db_name = os.getenv('DB_NAME', 'user_db')
    
    # Wait for database to be ready
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            conn = psycopg2.connect(
                host=db_host,
                database='postgres',
                user=db_user,
                password=db_password
            )
            conn.autocommit = True
            cursor = conn.cursor()
            
            # Check if database exists
            cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
            exists = cursor.fetchone()
            
            if not exists:
                cursor.execute(f'CREATE DATABASE {db_name}')
                print(f'Database {db_name} created successfully')
            else:
                print(f'Database {db_name} already exists')
            
            cursor.close()
            conn.close()
            return True
        except psycopg2.OperationalError as e:
            retry_count += 1
            print(f'Waiting for database... ({retry_count}/{max_retries})')
            time.sleep(1)
        except Exception as e:
            print(f'Error initializing database: {e}')
            return False
    
    print('Failed to connect to database after maximum retries')
    return False

if __name__ == '__main__':
    init_database()

