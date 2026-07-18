-- SQL: potencia con un CTE recursivo (ilustrativo, n=3).
WITH RECURSIVE p(i, v) AS (VALUES (0, 1) UNION ALL SELECT i + 1, v * 2 FROM p WHERE i < 3)
SELECT printf('resultado=%d', v) AS resultado FROM p ORDER BY i DESC LIMIT 1;
