-- SQL cuenta las filas (componentes).
WITH comps(nombre) AS (VALUES ('cli'), ('api'), ('web'))
SELECT printf('componentes=%d', count(*)) AS resultado FROM comps;
