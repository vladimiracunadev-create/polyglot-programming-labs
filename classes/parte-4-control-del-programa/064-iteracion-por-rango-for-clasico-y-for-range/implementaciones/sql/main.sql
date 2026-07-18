-- SQL: factorial con CTE recursivo (ilustrativo, n=5).
WITH RECURSIVE fact(i, f) AS (
    VALUES (1, 1)
    UNION ALL SELECT i + 1, f * (i + 1) FROM fact WHERE i < 5
)
SELECT printf('factorial=%d', f) AS resultado FROM fact ORDER BY i DESC LIMIT 1;
