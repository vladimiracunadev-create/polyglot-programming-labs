-- SQL calcula el cuadrado.
WITH nums(n) AS (VALUES (5), (0), (7))
SELECT printf('resultado=%d', n * n) AS resultado FROM nums;
