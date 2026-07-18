-- SQL: se evita la inyección con consultas parametrizadas; aquí, validación por patrón.
WITH t(w) AS (VALUES ('abc'))
SELECT printf('seguro=%s', CASE WHEN w GLOB '*[^A-Za-z0-9]*' THEN 'false' ELSE 'true' END) AS resultado FROM t;
