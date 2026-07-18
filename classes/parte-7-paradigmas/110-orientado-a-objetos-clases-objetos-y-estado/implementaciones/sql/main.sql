-- SQL no tiene objetos con estado; el contador es el propio valor.
WITH nums(n) AS (VALUES (5), (0), (3))
SELECT printf('cuenta=%d', n) AS resultado FROM nums;
