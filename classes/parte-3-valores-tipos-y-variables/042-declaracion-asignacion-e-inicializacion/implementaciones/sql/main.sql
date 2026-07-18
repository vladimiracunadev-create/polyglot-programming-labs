-- SQL no reasigna variables: se describe la salida intercambiando columnas.
WITH pares(a, b) AS (VALUES (3, 7), (0, 5), (-2, 9))
SELECT printf('a=%d b=%d', b, a) AS resultado
FROM pares;
