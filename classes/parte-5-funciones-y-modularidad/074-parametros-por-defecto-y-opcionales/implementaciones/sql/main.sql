-- SQL: COALESCE simula el valor por defecto (aquí, exponente 2 mediante base*base).
WITH datos(base) AS (VALUES (3), (5))
SELECT printf('resultado=%d', base * base) AS resultado FROM datos;
