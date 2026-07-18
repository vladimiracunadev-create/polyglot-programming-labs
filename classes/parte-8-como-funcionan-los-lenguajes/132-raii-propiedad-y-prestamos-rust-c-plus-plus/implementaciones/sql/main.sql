-- SQL no expone propiedad de memoria; se calcula el resultado.
WITH nums(n) AS (VALUES (5), (0), (7))
SELECT printf('resultado=%d', n * 2) AS resultado FROM nums;
