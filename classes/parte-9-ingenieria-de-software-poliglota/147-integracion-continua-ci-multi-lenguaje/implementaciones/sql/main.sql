-- SQL: verde si el mínimo de los pasos es 1.
WITH pasos(x) AS (VALUES (1), (1), (1))
SELECT printf('ci=%s', CASE WHEN min(x) = 1 THEN 'verde' ELSE 'rojo' END) AS resultado FROM pasos;
