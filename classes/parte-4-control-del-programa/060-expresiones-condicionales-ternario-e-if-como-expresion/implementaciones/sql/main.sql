-- SQL: la función max() elige el mayor directamente.
WITH pares(a, b) AS (VALUES (3, 7), (9, 2), (5, 5))
SELECT printf('max=%d', max(a, b)) AS resultado
FROM pares;
