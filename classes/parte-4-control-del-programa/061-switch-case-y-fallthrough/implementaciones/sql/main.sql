-- SQL: selección por valor con CASE WHEN.
WITH dias(d) AS (VALUES (1), (6), (8))
SELECT printf('dia=%s',
       CASE d WHEN 1 THEN 'lunes' WHEN 2 THEN 'martes' WHEN 3 THEN 'miercoles'
              WHEN 4 THEN 'jueves' WHEN 5 THEN 'viernes' WHEN 6 THEN 'sabado'
              WHEN 7 THEN 'domingo' ELSE 'invalido' END) AS resultado
FROM dias;
