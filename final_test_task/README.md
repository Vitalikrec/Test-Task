---

# ETL Project Documentation

## Overview

This project involves setting up an ETL process with Docker and PostgreSQL. The ETL process transforms data and inserts it into a PostgreSQL database. SQL queries are used to manipulate and analyze the data.

## Docker Setup

### Dockerfile

The `Dockerfile` is used to build the Docker image for the Python ETL application. It installs the required Python packages and sets up the environment.

### docker-compose.yml

The `docker-compose.yml` file defines the services for the application and PostgreSQL database. It specifies how to build the application container and configure the database.

### Instructions to Build and Run

1. **Navigate to the Project Directory**

   Before building the Docker images, change the directory to the root of this project folder, `final_test_task`, on your local machine:

   ```bash
   cd /path/to/final_test_task
   ```

2. **Build Docker Images**

   Run the following command to build the Docker images defined in `docker-compose.yml`:

   ```bash
   docker-compose build
   ```

3. **Start Containers**

   Run the following command to start the containers:

   ```bash
   docker-compose up
   ```

### Running ETL and SQL Scripts

- The `Dockerfile_app` uses the command `CMD ["python", "etl.py"]` to run only the ETL process.
- To run SQL scripts automatically after the ETL process, you can use:

  ```bash
  CMD ["sh", "-c", "python etl.py && python execute_sql.py"]
  ```

- To execute a SQL query manually, use:

  ```bash
  docker exec -i final_test_task-db-1 psql -U postgres -d postgres -f /app/queries/query2_unique_email_domains.sql
  ```

  Here, `final_test_task-db-1` is the container name, `postgres` is the user, `postgres` is the database, and `/app/queries/query2_unique_email_domains.sql` is the path to the SQL file you want to execute.

## Database Schema

### Schema and Table Creation

The schema and table are created using the `init.sql` script, which is run automatically when the PostgreSQL container starts. The schema and table definitions are as follows:

- **Schema:** `user_schema`
- **Table:** `users`
  - `user_id` (INT, PRIMARY KEY)
  - `name` (VARCHAR(200))
  - `email` (VARCHAR(200))
  - `signup_date` (DATE)
  - `domain` (VARCHAR(200))

## Assumptions and Verification

### Assumptions

- The PostgreSQL container is running and accessible on the default port (5432).
- The Python application container has access to the PostgreSQL container.
- The `init.sql` script is correctly setting up the schema and tables in PostgreSQL.

### How to Verify Results

1. **Check the PostgreSQL Database**

   Use the `psql` command-line tool or a PostgreSQL client to connect to the database and verify that the tables and schema have been created. You may need to enter the password found in `docker-compose.yml`.

   ```bash
   docker exec -it <container_id> psql -U postgres -d postgres
   ```

2. **Verify Data**

   Run SQL queries directly on the PostgreSQL database to ensure data has been correctly inserted and manipulated.

3. **Review Logs**

   Check the application logs for messages indicating successful execution of the ETL process and SQL queries.

   ```bash
   docker-compose logs app
   ```

---