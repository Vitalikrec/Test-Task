-- Delete records where the email domain is not from a specific list
DELETE FROM user_schema.users
WHERE domain NOT IN ('gmail.com', 'yahoo.com', 'example.com');
