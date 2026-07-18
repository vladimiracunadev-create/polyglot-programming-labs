-- SQL: varias columnas por fila son un multi-retorno natural.
WITH pares(a, b) AS (VALUES (17, 5), (10, 2), (7, 3))
SELECT printf('cociente=%d resto=%d', a / b, a % b) AS resultado FROM pares;
