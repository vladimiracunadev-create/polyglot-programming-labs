-- SQL llama a funciones definidas por el usuario; aqui, la expresion.
WITH nums(n) AS (VALUES (5), (0), (7))
SELECT printf('resultado=%d', n * 2) AS resultado FROM nums;
