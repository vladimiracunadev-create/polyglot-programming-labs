-- SQL: se inspeccionan los valores calculados.
WITH nums(n) AS (VALUES (3), (2), (5))
SELECT printf('valor=%d cuadrado=%d cubo=%d', n, n * n, n * n * n) AS resultado FROM nums;
