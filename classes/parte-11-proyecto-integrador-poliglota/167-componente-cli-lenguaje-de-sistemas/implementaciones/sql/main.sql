-- SQL no tiene CLI; se ilustra con valores.
WITH t(comando, args) AS (VALUES ('run', 2))
SELECT printf('comando=%s args=%d', comando, args) AS resultado FROM t;
