-- SQL evalúa la expresión numérica de forma uniforme.
WITH pares(a, b) AS (VALUES (2, 3.5), (10, 0.25), (0, 0))
SELECT printf('suma=%.2f', a + b) AS resultado
FROM pares;
