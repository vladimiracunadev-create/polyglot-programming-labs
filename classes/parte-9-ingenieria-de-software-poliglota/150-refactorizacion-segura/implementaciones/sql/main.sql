-- SQL: dos expresiones equivalentes.
WITH nums(n) AS (VALUES (5))
SELECT printf('equivalente=%s resultado=%d', CASE WHEN n * 2 = n + n THEN 'true' ELSE 'false' END, n + n) AS resultado FROM nums;
