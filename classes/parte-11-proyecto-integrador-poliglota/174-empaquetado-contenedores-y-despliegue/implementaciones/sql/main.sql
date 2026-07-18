-- SQL concatena el nombre de la imagen.
WITH t(v) AS (VALUES ('1.2.3'))
SELECT 'imagen=app:' || v AS resultado FROM t;
