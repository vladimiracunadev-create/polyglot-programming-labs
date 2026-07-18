-- SQL: coincidencia por rango con CASE WHEN.
WITH nums(n) AS (VALUES (5), (-3), (0))
SELECT printf('signo=%s',
       CASE WHEN n > 0 THEN 'positivo' WHEN n < 0 THEN 'negativo' ELSE 'cero' END) AS resultado
FROM nums;
