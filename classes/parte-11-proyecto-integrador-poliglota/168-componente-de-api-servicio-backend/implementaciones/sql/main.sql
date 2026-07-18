-- SQL devuelve filas; aqui, la respuesta simulada.
WITH t(n) AS (VALUES (5))
SELECT printf('respuesta=200 datos=%d', n) AS resultado FROM t;
