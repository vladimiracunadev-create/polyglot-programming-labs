-- SQL: el menor divisor > 1 con MIN sobre un rango (ilustrativo).
WITH RECURSIVE d(k) AS (VALUES (2) UNION ALL SELECT k + 1 FROM d WHERE k < 15)
SELECT printf('primer_divisor=%d', min(k)) AS resultado
FROM d WHERE 15 % k = 0;
