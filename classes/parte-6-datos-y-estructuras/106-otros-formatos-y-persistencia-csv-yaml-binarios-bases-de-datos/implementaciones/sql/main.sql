-- SQL: group_concat produce una fila CSV.
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT 'csv=' || group_concat(x, ',') || printf(' campos=%d', count(*)) AS resultado FROM nums;
