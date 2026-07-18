-- SQL: una consulta de comprobación.
WITH t(a, b, esperado) AS (VALUES (3, 4, 7))
SELECT printf('test=%s', CASE WHEN a + b = esperado THEN 'pasa' ELSE 'falla' END) AS resultado FROM t;
