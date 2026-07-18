-- SQL: sin pila explícita; evalúa la expresión.
WITH e(x, y, op) AS (VALUES (3, 4, '+'))
SELECT printf('resultado=%d', CASE op WHEN '+' THEN x + y WHEN '-' THEN x - y ELSE x * y END) AS resultado
FROM e;
