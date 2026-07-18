-- SQL: compara con la versión en minúsculas.
WITH t(w) AS (VALUES ('total'))
SELECT printf('valido=%s', CASE WHEN w = lower(w) THEN 'true' ELSE 'false' END) AS resultado FROM t;
