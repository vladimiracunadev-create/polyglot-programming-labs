-- SQL no tiene propiedad de memoria: opera sobre datos.
WITH palabras(s) AS (VALUES ('Ada'), ('Bo'), ('hola'))
SELECT printf('movido=%s longitud=%d', s, length(s)) AS resultado FROM palabras;
