-- SQL: selección por código con CASE.
WITH c(codigo) AS (VALUES (1))
SELECT printf('error=%s', CASE codigo WHEN 1 THEN 'sintaxis' WHEN 2 THEN 'tipos' WHEN 3 THEN 'enlace' WHEN 4 THEN 'ejecucion' ELSE 'desconocido' END) AS resultado
FROM c;
