-- SQL: se perfila con EXPLAIN; aquí, conteo y suma.
WITH RECURSIVE r(i) AS (VALUES (1) UNION ALL SELECT i + 1 FROM r WHERE i < 5)
SELECT printf('operaciones=%d resultado=%d', count(*), sum(i)) AS resultado FROM r;
