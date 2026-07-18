-- SQL: selecciona la estrategia con CASE.
WITH t(e, a, b) AS (VALUES ('suma', 3, 4))
SELECT printf('resultado=%d', CASE e WHEN 'suma' THEN a + b WHEN 'resta' THEN a - b ELSE a * b END) AS resultado FROM t;
