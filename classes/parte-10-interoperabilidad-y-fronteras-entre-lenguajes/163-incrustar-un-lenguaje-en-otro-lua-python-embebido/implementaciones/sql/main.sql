-- SQL se embebe en apps via librerias cliente; aqui, la suma.
WITH t(a, b) AS (VALUES (3, 4))
SELECT printf('resultado=%d', a + b) AS resultado FROM t;
