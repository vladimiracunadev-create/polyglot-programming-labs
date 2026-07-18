-- SQL: una fila de una tabla es un registro.
WITH personas(nombre, edad) AS (VALUES ('Ada', 36))
SELECT printf('Persona(nombre=%s, edad=%d)', nombre, edad) AS resultado FROM personas;
