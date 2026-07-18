-- SQL: concatena el prefijo con ||.
WITH t(v) AS (VALUES ('1.2.3'))
SELECT 'desplegado=v' || v AS resultado FROM t;
