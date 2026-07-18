-- SQL automatiza con procedimientos/trabajos; aqui, el conteo.
WITH t(n) AS (VALUES (5))
SELECT printf('tareas=%d estado=completado', n) AS resultado FROM t;
