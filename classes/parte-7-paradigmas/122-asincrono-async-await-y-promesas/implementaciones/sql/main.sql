-- SQL no tiene async a nivel de lenguaje.
WITH nums(n) AS (VALUES (5), (0), (6))
SELECT printf('resultado=%d', n * 2) AS resultado FROM nums;
