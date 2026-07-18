-- SQL: suma 1..n con un CTE recursivo (ilustrativo, n=10).
WITH RECURSIVE seq(i) AS (
    VALUES (1)
    UNION ALL SELECT i + 1 FROM seq WHERE i < 10
)
SELECT printf('suma=%d', sum(i)) AS resultado FROM seq;
