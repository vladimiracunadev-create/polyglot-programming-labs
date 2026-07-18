-- SQL: GROUP BY para frecuencias.
WITH nums(x) AS (VALUES (3), (1), (3), (3))
SELECT printf('cuenta=%d', count(*)) AS resultado
FROM nums WHERE x = (SELECT x FROM nums LIMIT 1);
