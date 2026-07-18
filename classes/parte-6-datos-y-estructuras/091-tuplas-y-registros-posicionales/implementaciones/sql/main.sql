-- SQL: una fila con varias columnas es una tupla.
WITH pares(a, b) AS (VALUES (3, 4), (0, -2), (5, 5))
SELECT printf('tupla=(%d, %d)', b, a) AS resultado FROM pares;
