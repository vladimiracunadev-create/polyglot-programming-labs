-- SQL: cuenta las filas (módulos).
WITH mods(nombre) AS (VALUES ('a'), ('b'), ('c'))
SELECT printf('complejidad=%d', count(*)) AS resultado FROM mods;
