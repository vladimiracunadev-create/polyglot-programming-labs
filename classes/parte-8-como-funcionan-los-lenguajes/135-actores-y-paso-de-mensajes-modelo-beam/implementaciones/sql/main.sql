-- SQL agrega sin actores; SUM sobre las filas.
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT printf('total=%d', sum(x)) AS resultado FROM nums;
