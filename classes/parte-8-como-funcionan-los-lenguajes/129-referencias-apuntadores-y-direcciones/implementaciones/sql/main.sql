-- SQL: acceso por posición con una subconsulta ordenada (ilustrativo).
WITH datos(pos, x) AS (VALUES (0, 10), (1, 20), (2, 30))
SELECT printf('valor=%d', x) AS resultado FROM datos WHERE pos = 1;
