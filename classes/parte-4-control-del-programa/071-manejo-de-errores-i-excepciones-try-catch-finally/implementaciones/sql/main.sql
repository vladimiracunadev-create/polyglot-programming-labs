-- SQL: evita el error comprobando el divisor con CASE WHEN.
WITH pares(a, b) AS (VALUES (10, 2), (7, 0), (9, 3))
SELECT CASE WHEN b = 0 THEN 'error=division por cero'
            ELSE printf('resultado=%d', a / b) END AS resultado
FROM pares;
