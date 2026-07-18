-- SQL: agregacion declarativa con SUM.
WITH datos(x) AS (VALUES (10), (20), (30))
SELECT printf('total=%d', sum(x)) AS resultado FROM datos;
