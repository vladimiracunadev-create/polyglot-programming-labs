-- SQL: longitud con length(); palabras con funciones de texto (ilustrativo).
WITH t(linea) AS (VALUES ('hola mundo'))
SELECT printf('palabras=%d caracteres=%d',
       length(linea) - length(replace(linea, ' ', '')) + 1, length(linea)) AS resultado
FROM t;
