-- SQL: sin tipo de error; se distingue el caso con CASE WHEN.
WITH pares(a, b) AS (VALUES (10, 2), (7, 0), (8, 4))
SELECT CASE WHEN b = 0 THEN 'err=division'
            ELSE printf('ok=%d', a / b) END AS resultado
FROM pares;
