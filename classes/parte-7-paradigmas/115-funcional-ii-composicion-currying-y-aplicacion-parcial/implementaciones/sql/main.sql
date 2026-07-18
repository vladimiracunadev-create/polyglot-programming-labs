-- SQL: se anidan las expresiones/funciones.
WITH nums(n) AS (VALUES (5), (0), (3))
SELECT printf('resultado=%d', (n * 2) + 1) AS resultado FROM nums;
