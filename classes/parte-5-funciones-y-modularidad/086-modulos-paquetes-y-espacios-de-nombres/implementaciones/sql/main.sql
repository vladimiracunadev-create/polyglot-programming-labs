-- SQL organiza en esquemas (schemas); la operación va en la consulta.
WITH nums(n) AS (VALUES (5), (0), (-4))
SELECT printf('resultado=%d', 2 * n) AS resultado FROM nums;
