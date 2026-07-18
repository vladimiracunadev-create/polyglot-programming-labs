-- SQL propaga NULL por las operaciones automáticamente.
WITH nums(n) AS (VALUES (5), (0), (-3))
SELECT CASE WHEN n > 0 THEN printf('resultado=%d', n * 2) ELSE 'resultado=nada' END AS resultado
FROM nums;
