-- SQL: CAST(x AS INTEGER) trunca hacia cero.
WITH nums(x) AS (VALUES (3.7), (5.0), (8.9))
SELECT printf('entero=%d real=%.2f', CAST(x AS INTEGER), x) AS resultado
FROM nums;
