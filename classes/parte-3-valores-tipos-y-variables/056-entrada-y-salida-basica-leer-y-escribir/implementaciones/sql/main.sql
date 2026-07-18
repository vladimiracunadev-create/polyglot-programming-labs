-- SQL no lee stdin: se muestra el eco sobre una tabla de textos.
WITH lineas(x) AS (VALUES ('hola'), ('Polyglot'), ('123'))
SELECT printf('eco: %s', x) AS resultado
FROM lineas;
