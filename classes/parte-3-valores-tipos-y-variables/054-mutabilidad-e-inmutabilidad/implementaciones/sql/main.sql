-- SQL construye la secuencia con un CTE recursivo y group_concat (ilustrativo, n=5).
WITH RECURSIVE seq(i) AS (
    VALUES (1)
    UNION ALL SELECT i + 1 FROM seq WHERE i < 5
)
SELECT 'sec=' || group_concat(i, '-') AS resultado FROM seq;
