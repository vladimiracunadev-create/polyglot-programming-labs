-- SQL: filtra con WHERE.
WITH nums(x) AS (VALUES (1), (2), (3), (4))
SELECT 'pares=' || group_concat(x, '-') AS resultado FROM nums WHERE x % 2 = 0;
