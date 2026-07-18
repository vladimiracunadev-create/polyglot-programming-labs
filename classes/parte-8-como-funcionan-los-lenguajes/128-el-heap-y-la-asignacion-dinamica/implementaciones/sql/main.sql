-- SQL: genera la secuencia descendente con un CTE (ilustrativo, n=3).
WITH RECURSIVE r(i) AS (VALUES (3) UNION ALL SELECT i - 1 FROM r WHERE i > 1)
SELECT 'lista=' || group_concat(i, '-') AS resultado FROM r;
