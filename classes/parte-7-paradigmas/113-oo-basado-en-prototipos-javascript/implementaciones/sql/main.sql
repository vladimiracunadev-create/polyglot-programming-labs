-- SQL no tiene objetos; el cálculo va en la consulta.
WITH nums(n) AS (VALUES (5), (0), (7))
SELECT printf('resultado=%d', n * 2) AS resultado FROM nums;
