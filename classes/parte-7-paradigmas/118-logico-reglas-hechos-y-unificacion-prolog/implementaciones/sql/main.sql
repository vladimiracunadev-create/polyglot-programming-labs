-- SQL (declarativo, primo del lógico): la condición como CASE.
WITH pares(a, b) AS (VALUES (3, 12), (5, 12), (4, 12))
SELECT printf('divisor=%s', CASE WHEN b % a = 0 THEN 'true' ELSE 'false' END) AS resultado FROM pares;
