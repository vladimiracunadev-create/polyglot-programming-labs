-- SQL: MAX agrega sobre las filas.
WITH nums(x) AS (VALUES (3), (1), (4))
SELECT printf('max=%d', max(x)) AS resultado FROM nums;
