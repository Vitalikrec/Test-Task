-- Retrieve the count of users who signed up on each day
SELECT signup_date AS signup_day, COUNT(*) AS user_count
FROM user_schema.users
GROUP BY signup_date
ORDER BY signup_day;
