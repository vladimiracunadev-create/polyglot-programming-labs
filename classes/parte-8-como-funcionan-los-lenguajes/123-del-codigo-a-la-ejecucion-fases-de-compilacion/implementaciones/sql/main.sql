-- SQL evalúa la expresión según el operador con CASE.
WITH e(a, op, b) AS (VALUES (3, '+', 4))
SELECT printf('resultado=%d', CASE op WHEN '+' THEN a + b WHEN '-' THEN a - b ELSE a * b END) AS resultado
FROM e;
