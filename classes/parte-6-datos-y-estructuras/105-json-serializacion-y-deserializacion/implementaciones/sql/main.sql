-- SQL: construye JSON con printf (o json_object en motores con la extensión).
WITH personas(nombre, edad) AS (VALUES ('Ada', 36))
SELECT printf('{"nombre": "%s", "edad": %d}', nombre, edad) AS resultado FROM personas;
