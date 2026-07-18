-- SQL: COUNT(DISTINCT x).
WITH nums(x) AS (VALUES (1), (2), (2), (3), (3), (3))
SELECT printf('unicos=%d', count(DISTINCT x)) AS resultado FROM nums;
