-- SQL: recursión con CTE (ilustrativo, n=5).
WITH RECURSIVE r(i) AS (VALUES (1) UNION ALL SELECT i + 1 FROM r WHERE i < 5)
SELECT printf('suma=%d profundidad=%d', sum(i), max(i)) AS resultado FROM r;
