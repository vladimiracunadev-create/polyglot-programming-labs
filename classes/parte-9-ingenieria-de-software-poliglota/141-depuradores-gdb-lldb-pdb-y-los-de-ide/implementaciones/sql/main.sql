-- SQL: sumas acumuladas con función de ventana (ilustrativo, n=3).
WITH RECURSIVE r(i) AS (VALUES (1) UNION ALL SELECT i + 1 FROM r WHERE i < 3)
SELECT 'traza=' || group_concat(s, '-') AS resultado
FROM (SELECT sum(i) OVER (ORDER BY i) AS s FROM r);
