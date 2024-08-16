import os
import pandas as pd
from datetime import datetime
import time
from faker import Faker
import random
import re
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


# Logger
def log_progress(message):
    with open('/app/logs/code_log.txt', 'a') as log_file:
        time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_file.write(f"{time_stamp} : {message}\n")


# Step 1: Generate CSV file
def generate_csv(num_records, domains, generate_csv_path):
    try:
        # Create an instance of the Faker class for generating fake data
        fake = Faker()
        # Initialize an empty list to store the generated data
        data = []
        # Generate the specified number of records
        for i in range(1, num_records + 1):
            user_id = i
            name = fake.name()
            email = f"{fake.user_name()}@{random.choice(domains)}"
            # Generate a random signup date as a Unix timestamp
            signup_date = fake.date_time_this_decade().timestamp()
            data.append([user_id, name, email, signup_date])

        # Convert the list of data into a pandas DataFrame with specified column names
        df = pd.DataFrame(data, columns=['user_id', 'name', 'email', 'signup_date'])
        df.to_csv(generate_csv_path, index=False)
        log_progress("CSV file successfully generated!")
    except Exception as e:
        log_progress(f"Error generating CSV file: {e}")


# Step 2: Extract Data
def extract_data(generate_csv_path):
    try:
        # Extract Data from generated csv file
        extracted_data = pd.read_csv(generate_csv_path)
        log_progress('Extraction completed')
        return extracted_data
    except Exception as e:
        log_progress(f"Error during data extraction: {e}")


# Step 3: Transform the data
def transform_data(df):
    try:
        # Convert 'signup_date' from seconds since epoch to a human-readable date format (YYYY-MM-DD)
        df['signup_date'] = pd.to_datetime(df['signup_date'], unit='s').dt.strftime('%Y-%m-%d')
        # Define a regex pattern for validating email addresses
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        # Filter rows to keep only those with valid email addresses
        df = df[df['email'].apply(lambda x: re.match(email_pattern, x) is not None)]
        # Extract the domain part of the email addresses and store it in a new column 'domain'
        df['domain'] = df['email'].apply(lambda x: x.split('@')[1])
        log_progress('Transformation completed')
        return df
    except Exception as e:
        log_progress(f"Error during data transformation: {e}")



# Step 4: Load data
def load_data(db_params, transformed_df, table_name, schema):
    try:
        time.sleep(5)
        # Create a SQLAlchemy engine for connecting to the PostgreSQL database
        engine = create_engine(f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}")
        # Write the DataFrame 'transformed_df' to the specified PostgreSQL table
        transformed_df.to_sql(table_name, engine, schema=schema, if_exists='append', index=False)
        log_progress(f"Data inserted successfully into the {table_name} table!")
    except SQLAlchemyError as e:
        log_progress(f"Error inserting data {e}")


# Main execution
if __name__ == "__main__":

    num_records = 1000
    domains = ['gmail.com', 'yahoo.com', 'example.com', 'company.com', 'hotmail.com']
    generated_csv_path = '/app/csv_files/generated_users.csv'
    
    # Initial DB parameters
    db_params = {
        'host': os.getenv('DB_HOST'),
        'database': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'port': os.getenv('DB_PORT')
    }
    
    # Step 1: Generate CSV
    generate_csv(num_records, domains, generated_csv_path)
    
    # Step 2: Extract Data
    extracted_data = extract_data(generated_csv_path)

    # Step 3: Transform Data
    transformed_df = transform_data(extracted_data)

    # Step 4: Load Data into DB
    # Ensure that the table name and schema match those specified in `init.sql`
    load_data(db_params, transformed_df, table_name='users', schema='user_schema')
    