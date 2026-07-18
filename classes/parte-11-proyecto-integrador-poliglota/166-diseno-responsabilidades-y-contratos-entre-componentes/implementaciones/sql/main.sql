-- SQL compara los valores de contrato.
WITH t(a, b) AS (VALUES (5, 5))
SELECT printf('contrato=%s', CASE WHEN a = b THEN 'compatible' ELSE 'incompatible' END) AS resultado FROM t;
