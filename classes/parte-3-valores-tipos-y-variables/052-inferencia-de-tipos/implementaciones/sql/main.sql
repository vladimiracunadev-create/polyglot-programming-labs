-- SQL: la expresión produce el valor sin declarar variables.
WITH pares(a, b) AS (VALUES (3, 4), (0, 9), (-2, 5))
SELECT printf('producto=%d', a * b) AS resultado
FROM pares;
