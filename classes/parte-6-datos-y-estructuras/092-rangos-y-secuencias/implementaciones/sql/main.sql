-- SQL: rango con CTE recursivo (ilustrativo, 2..5).
WITH RECURSIVE r(i) AS (VALUES (2) UNION ALL SELECT i + 1 FROM r WHERE i < 5)
SELECT 'rango=' || group_concat(i, '-') || printf(' suma=%d', sum(i)) AS resultado FROM r;
