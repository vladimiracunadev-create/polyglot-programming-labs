-- SQL cuenta y une los componentes.
WITH c(nombre) AS (VALUES ('cli'), ('api'), ('web'))
SELECT printf('componentes=%d nombres=%s', count(*), group_concat(nombre, '-')) AS resultado FROM c;
