-- SQL: invierte con ORDER BY sobre la posición.
WITH nums(pos, x) AS (VALUES (1, 1), (2, 2), (3, 3))
SELECT 'invertido=' || group_concat(x, '-') AS resultado
FROM (SELECT x FROM nums ORDER BY pos DESC);
