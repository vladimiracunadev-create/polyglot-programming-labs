-- SQL se documenta con comentarios; aqui, el conteo.
WITH t(n) AS (VALUES (5))
SELECT printf('documentado=%d secciones', n) AS resultado FROM t;
