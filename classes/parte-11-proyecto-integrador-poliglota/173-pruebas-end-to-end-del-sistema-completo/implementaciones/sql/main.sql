-- SQL prueba con una consulta de comprobacion.
WITH t(a, b, esperado) AS (VALUES (3, 4, 7))
SELECT printf('e2e=%s', CASE WHEN a + b = esperado THEN 'pasa' ELSE 'falla' END) AS resultado FROM t;
