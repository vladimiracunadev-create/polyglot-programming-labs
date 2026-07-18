-- SQL: ORDER BY equivale al in-order del BST.
WITH nums(x) AS (VALUES (3), (1), (4))
SELECT 'inorden=' || group_concat(x, '-') AS resultado
FROM (SELECT x FROM nums ORDER BY x);
