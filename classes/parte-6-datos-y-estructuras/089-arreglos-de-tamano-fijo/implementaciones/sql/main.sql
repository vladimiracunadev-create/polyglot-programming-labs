-- SQL: agrega sobre filas, no índices.
WITH arr(x) AS (VALUES (3), (1), (4))
SELECT printf('suma=%d max=%d', sum(x), max(x)) AS resultado FROM arr;
