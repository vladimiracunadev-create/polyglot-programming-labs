-- SQL (declarativo): suma con CTE recursivo (ilustrativo, n=5).
WITH RECURSIVE r(i) AS (VALUES (1) UNION ALL SELECT i + 1 FROM r WHERE i < 5)
SELECT printf('suma=%d', sum(i)) AS resultado FROM r;
