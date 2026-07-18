-- SQL: SUM() agrega filas, no argumentos variádicos.
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT printf('suma=%d', sum(x)) AS resultado FROM nums;
