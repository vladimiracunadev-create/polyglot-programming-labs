-- SQL usa operadores/funciones incorporadas, no funciones como valor.
WITH pares(a, b) AS (VALUES (3, 4), (5, 5), (0, 9))
SELECT printf('suma=%d producto=%d', a + b, a * b) AS resultado FROM pares;
