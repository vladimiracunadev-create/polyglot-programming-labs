-- SQL: sin interfaces; se usa CASE.
WITH formas(tipo, a, b) AS (VALUES ('cuadrado', 5, 0))
SELECT printf('area=%d', CASE WHEN tipo = 'cuadrado' THEN a * a ELSE a * b END) AS resultado FROM formas;
