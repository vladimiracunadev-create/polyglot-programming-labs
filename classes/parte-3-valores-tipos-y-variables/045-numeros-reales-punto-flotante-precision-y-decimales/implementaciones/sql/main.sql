-- SQL formatea reales con printf dentro de la consulta.
WITH pares(a, b) AS (VALUES (1.5, 2.5), (0.1, 0.2), (10, 3))
SELECT printf('suma=%.2f producto=%.2f', a + b, a * b) AS resultado
FROM pares;
