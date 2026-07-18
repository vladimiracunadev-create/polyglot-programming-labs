-- SQL: genera los pares con un CTE recursivo (ilustrativo, n=5).
WITH RECURSIVE pares(i, v) AS (
    VALUES (1, 2)
    UNION ALL SELECT i + 1, (i + 1) * 2 FROM pares WHERE i < 5
)
SELECT 'pares=' || group_concat(v, '-') AS resultado FROM pares;
