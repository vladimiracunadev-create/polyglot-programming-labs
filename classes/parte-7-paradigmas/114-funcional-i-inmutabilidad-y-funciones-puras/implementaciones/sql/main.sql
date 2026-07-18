-- SQL: la transformación va en el SELECT, sin mutar.
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT 'doblados=' || group_concat(x * 2, '-') AS resultado FROM nums;
