-- SQL usa alias/subconsultas para acotar nombres.
WITH nums(n) AS (VALUES (5), (0), (-3))
SELECT printf('interno=%d externo=%d', n + 10, n) AS resultado FROM nums;
