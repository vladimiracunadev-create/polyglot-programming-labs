-- SQL no tiene un tipo booleano nativo universal: se usa CASE WHEN.
WITH nums(n) AS (VALUES (4), (7), (0))
SELECT printf('entero=%d real=%.1f par=%s', n, n,
       CASE WHEN n % 2 = 0 THEN 'true' ELSE 'false' END) AS resultado
FROM nums;
