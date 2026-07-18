-- SQL no tiene cierres: se parametriza con valores en la consulta.
WITH bases(base) AS (VALUES (10), (0), (100))
SELECT printf('r1=%d r2=%d', base + 1, base + 2) AS resultado FROM bases;
