-- SQL: COUNT sobre las filas.
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT printf('cuenta=%d', count(*)) AS resultado FROM nums;
