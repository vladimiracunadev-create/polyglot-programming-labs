-- SQL: la operación se expresa en la propia consulta.
WITH pares(a, b) AS (VALUES (3, 4), (10, 20), (-5, 5))
SELECT printf('suma=%d', a + b) AS resultado FROM pares;
