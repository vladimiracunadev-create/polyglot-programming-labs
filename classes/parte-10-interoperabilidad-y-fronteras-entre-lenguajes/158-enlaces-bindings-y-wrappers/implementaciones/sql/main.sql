-- SQL usa vistas para envolver; aqui, la expresion formateada.
WITH nums(n) AS (VALUES (5), (0), (7))
SELECT printf('envuelto=wrap(%d)', n * 2) AS resultado FROM nums;
