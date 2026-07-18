-- SQL compara los anchos.
WITH t(a, b) AS (VALUES (64, 64))
SELECT printf('abi=%s', CASE WHEN a = b THEN 'compatible' ELSE 'incompatible' END) AS resultado FROM t;
