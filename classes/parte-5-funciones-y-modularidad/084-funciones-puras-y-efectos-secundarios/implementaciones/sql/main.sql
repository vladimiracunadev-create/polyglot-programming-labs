-- SQL (declarativo) favorece expresiones puras.
WITH nums(n) AS (VALUES (4), (-3), (0))
SELECT printf('puro=%d', n * n) AS resultado FROM nums;
