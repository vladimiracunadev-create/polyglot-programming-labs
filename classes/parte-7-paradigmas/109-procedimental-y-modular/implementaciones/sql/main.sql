-- SQL: AVG con división entera.
WITH nums(x) AS (VALUES (2), (4), (6))
SELECT printf('promedio=%d', sum(x) / count(*)) AS resultado FROM nums;
