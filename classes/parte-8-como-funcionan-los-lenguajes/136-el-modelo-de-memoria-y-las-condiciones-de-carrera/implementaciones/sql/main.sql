-- SQL usa transacciones para la consistencia; aquí, el conteo.
WITH nums(n) AS (VALUES (5), (0), (3))
SELECT printf('cuenta=%d', n) AS resultado FROM nums;
