-- SQL: SUM() agrega sobre las filas, sin bucle.
WITH nums(x) AS (VALUES (3), (1), (4))
SELECT printf('suma=%d', sum(x)) AS resultado FROM nums;
