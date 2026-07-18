-- SQL construye el endpoint por concatenacion.
WITH t(metodo, recurso) AS (VALUES ('GET', 'users'))
SELECT 'contrato=' || metodo || ' /' || recurso AS resultado FROM t;
