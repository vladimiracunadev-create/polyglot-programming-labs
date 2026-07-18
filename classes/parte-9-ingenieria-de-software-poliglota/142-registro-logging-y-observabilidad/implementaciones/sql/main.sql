-- SQL: registro con una tabla/consulta de auditoría.
WITH t(n) AS (VALUES (5))
SELECT printf('log=[INFO] procesados=%d', n) AS resultado FROM t;
