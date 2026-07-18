-- SQL: sin despacho polimórfico; se usa CASE.
WITH animales(tipo) AS (VALUES ('perro'))
SELECT printf('sonido=%s', CASE tipo WHEN 'perro' THEN 'guau' WHEN 'gato' THEN 'miau' ELSE 'muu' END) AS resultado
FROM animales;
