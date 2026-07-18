-- SQL: WHERE + SELECT es un pipeline declarativo.
WITH nums(x) AS (VALUES (1), (2), (3), (4))
SELECT 'stream=' || group_concat(x * 2, '-') AS resultado FROM nums WHERE x % 2 = 0;
