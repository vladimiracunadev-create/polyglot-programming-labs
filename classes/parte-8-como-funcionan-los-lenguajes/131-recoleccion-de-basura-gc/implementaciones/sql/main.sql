-- SQL no expone la memoria; se informa el conteo.
WITH nums(n) AS (VALUES (5), (0), (3))
SELECT printf('creados=%d estado=recolectado', n) AS resultado FROM nums;
