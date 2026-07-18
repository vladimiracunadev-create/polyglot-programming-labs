-- SQL: condiciones con AND dentro de CASE WHEN.
WITH nums(n) AS (VALUES (4), (-3), (7))
SELECT printf('positivo=%s par=%s ambos=%s',
       CASE WHEN n > 0 THEN 'true' ELSE 'false' END,
       CASE WHEN n % 2 = 0 THEN 'true' ELSE 'false' END,
       CASE WHEN n > 0 AND n % 2 = 0 THEN 'true' ELSE 'false' END) AS resultado
FROM nums;
