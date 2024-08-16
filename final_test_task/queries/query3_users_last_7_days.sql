-- Retrieve the details of users whose signup_date is within the last 7 days
SELECT *
FROM user_schema.users
WHERE signup_date >= (
    SELECT MAX(signup_date) - INTERVAL '7 days'
    FROM user_schema.users
);