-- SQL: cuenta las filas (capas).
WITH capas(nombre) AS (VALUES ('web'), ('api'), ('datos'))
SELECT printf('capas=%d', count(*)) AS resultado FROM capas;
