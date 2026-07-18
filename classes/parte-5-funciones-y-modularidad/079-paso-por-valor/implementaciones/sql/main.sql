-- SQL: sin variables del llamador; la expresión produce el valor.
WITH nums(n) AS (VALUES (5), (3), (0))
SELECT printf('original=%d local=%d', n, n * 2) AS resultado FROM nums;
