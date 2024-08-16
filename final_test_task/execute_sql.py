import os
import psycopg2
from etl import log_progress

def execute_sql_queries(db_params, queries_dir):
    conn = None
    cur = None
    
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=db_params['database'],
            user=db_params['user'],
            password=db_params['password'],
            host=db_params['host'],
            port=db_params['port']
        )
        cur = conn.cursor()
        
        # Execute each SQL file in the queries directory
        for file_name in os.listdir(queries_dir):
            if file_name.endswith('.sql'):
                file_path = os.path.join(queries_dir, file_name)
                try:
                    with open(file_path, 'r') as sql_file:
                        cur.execute(sql_file.read())
                        conn.commit()
                        log_progress(f"Executed {file_name} successfully.")
                except Exception as inner_e:
                    conn.rollback()
                    log_progress(f"Failed to execute {file_name}: {inner_e}")
                            
    except Exception as e:
        log_progress(f"Error executing SQL queries: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
            
            

if __name__ == "__main__":
    
    db_params = {
        'host': os.getenv('DB_HOST'),
        'database': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'port': os.getenv('DB_PORT')
    }
    queries_dir = '/app/queries'
    execute_sql_queries(db_params, queries_dir)
