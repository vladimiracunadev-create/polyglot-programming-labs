-- SQL: clasificación con CASE WHEN en orden.
WITH edades(edad) AS (VALUES (-5), (10), (20))
SELECT CASE WHEN edad < 0 THEN 'invalido'
            WHEN edad < 18 THEN 'menor'
            ELSE 'adulto' END AS resultado
FROM edades;
