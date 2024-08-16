-- Find the user(s) with the most common email domain
SELECT *
FROM user_schema.users
WHERE domain = (
    SELECT domain
    FROM user_schema.users
    GROUP BY domain
    ORDER BY COUNT(*) DESC
    LIMIT 1
);
