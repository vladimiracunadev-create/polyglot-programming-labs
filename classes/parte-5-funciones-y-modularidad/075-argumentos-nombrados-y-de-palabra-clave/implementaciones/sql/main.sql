-- SQL nombra columnas, análogo a nombrar argumentos.
WITH puntos(x, y) AS (VALUES (3, 4), (0, -2), (5, 5))
SELECT printf('punto(x=%d, y=%d)', x, y) AS resultado FROM puntos;
