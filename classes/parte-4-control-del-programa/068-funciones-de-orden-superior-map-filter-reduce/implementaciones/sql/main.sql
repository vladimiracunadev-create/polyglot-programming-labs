-- SQL: el 'map' va en el SELECT y el 'reduce' con SUM().
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT 'doblados=' || group_concat(x * 2, '-') || printf(' total=%d', sum(x * 2)) AS resultado
FROM nums;
