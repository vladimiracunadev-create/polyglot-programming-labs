-- SQL: compara dos valores.
WITH t(x, y) AS (VALUES (6, 6))
SELECT printf('equivalente=%s', CASE WHEN x = y THEN 'true' ELSE 'false' END) AS resultado FROM t;
