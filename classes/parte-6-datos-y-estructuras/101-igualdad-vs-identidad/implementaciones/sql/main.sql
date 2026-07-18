-- SQL: compara valores con =.
WITH pares(a, b) AS (VALUES (5, 5), (3, 7), (0, 0))
SELECT printf('iguales=%s', CASE WHEN a = b THEN 'true' ELSE 'false' END) AS resultado FROM pares;
