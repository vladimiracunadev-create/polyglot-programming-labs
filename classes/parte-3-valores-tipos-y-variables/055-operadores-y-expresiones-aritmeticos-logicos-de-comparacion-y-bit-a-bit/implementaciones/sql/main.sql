-- SQL evalúa las operaciones aritméticas en la consulta (/ entre enteros es división entera).
WITH pares(a, b) AS (VALUES (10, 3), (20, 4), (7, 2))
SELECT printf('suma=%d resta=%d mult=%d div=%d mod=%d', a + b, a - b, a * b, a / b, a % b) AS resultado
FROM pares;
