-- SQL no tiene tipo booleano nativo: se expresa con CASE WHEN.
WITH pares(a, b) AS (VALUES (1, 0), (1, 1), (0, 0))
SELECT printf('and=%s or=%s not_a=%s',
       CASE WHEN a <> 0 AND b <> 0 THEN 'true' ELSE 'false' END,
       CASE WHEN a <> 0 OR b <> 0 THEN 'true' ELSE 'false' END,
       CASE WHEN NOT (a <> 0) THEN 'true' ELSE 'false' END) AS resultado
FROM pares;
