-- SQL persiste en tablas; aqui, el par guardado.
WITH t(clave, valor) AS (VALUES ('x', '5'))
SELECT 'guardado=' || clave || '=' || valor AS resultado FROM t;
