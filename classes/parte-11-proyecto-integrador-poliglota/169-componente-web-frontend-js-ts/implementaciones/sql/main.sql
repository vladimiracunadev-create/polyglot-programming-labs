-- SQL provee datos; aqui, el render simulado.
WITH t(n) AS (VALUES (3))
SELECT printf('items=%d render=ok', n) AS resultado FROM t;
