-- SQL: length(w) cuenta los caracteres de una cadena.
WITH palabras(w) AS (VALUES ('Ada'), ('Bo'), ('polyglot'))
SELECT printf('hola=%s longitud=%d', w, length(w)) AS resultado
FROM palabras;
