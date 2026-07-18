-- SQL concatena clave y valor.
WITH t(clave, valor) AS (VALUES ('x', '5'))
SELECT 'serializado=' || clave || ':' || valor AS resultado FROM t;
