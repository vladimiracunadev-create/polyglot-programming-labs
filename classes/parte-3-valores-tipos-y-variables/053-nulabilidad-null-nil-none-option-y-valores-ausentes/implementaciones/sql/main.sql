-- SQL tiene NULL nativo; aquí 0 modela la ausencia con CASE WHEN.
WITH nums(n) AS (VALUES (5), (0), (42))
SELECT CASE WHEN n = 0 THEN 'valor=ausente' ELSE printf('valor=%d', n) END AS resultado
FROM nums;
