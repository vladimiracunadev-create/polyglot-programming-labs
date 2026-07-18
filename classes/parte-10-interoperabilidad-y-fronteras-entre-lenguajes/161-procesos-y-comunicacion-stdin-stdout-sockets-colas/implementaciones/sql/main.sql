-- SQL agrega los mensajes con SUM.
WITH cola(x) AS (VALUES (1), (2), (3))
SELECT printf('recibido=%d', sum(x)) AS resultado FROM cola;
