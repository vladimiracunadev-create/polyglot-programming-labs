-- SQL no tiene eventos; se genera la secuencia con un CTE (ilustrativo, n=3).
WITH RECURSIVE e(i) AS (VALUES (1) UNION ALL SELECT i + 1 FROM e WHERE i < 3)
SELECT 'eventos=' || group_concat(i, '-') AS resultado FROM e;
