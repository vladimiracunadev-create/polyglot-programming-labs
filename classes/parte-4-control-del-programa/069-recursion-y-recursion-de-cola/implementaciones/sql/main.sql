-- SQL: Fibonacci con un CTE recursivo (ilustrativo, n=10).
WITH RECURSIVE fib(i, a, b) AS (
    VALUES (0, 0, 1)
    UNION ALL SELECT i + 1, b, a + b FROM fib WHERE i < 10
)
SELECT printf('fib=%d', a) AS resultado FROM fib WHERE i = 10;
