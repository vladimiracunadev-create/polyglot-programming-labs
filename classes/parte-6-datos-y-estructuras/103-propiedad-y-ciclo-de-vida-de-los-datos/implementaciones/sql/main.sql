-- SQL: el ciclo de vida se gestiona con transacciones; aquí se ilustra el valor.
WITH nums(n) AS (VALUES (5), (0), (9))
SELECT printf('valor=%d estado=liberado', n) AS resultado FROM nums;
