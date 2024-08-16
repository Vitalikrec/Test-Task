CREATE SCHEMA user_schema

CREATE TABLE user_schema.users (
                user_id INT PRIMARY KEY,
                name VARCHAR(200),
                email VARCHAR(200),
                signup_date DATE,
                domain VARCHAR(200)
);

