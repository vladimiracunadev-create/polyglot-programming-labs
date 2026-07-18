-- SQL: aristas = filas de pares; nodos = valores distintos.
WITH nums(x) AS (VALUES (1), (2), (2), (3))
SELECT printf('aristas=%d nodos=%d', count(*) / 2, count(DISTINCT x)) AS resultado FROM nums;
