-- SQL (sqlite) solo formatea hexadecimal con %x; octal y binario no son nativos.
WITH nums(n) AS (VALUES (255), (10), (1))
SELECT printf('dec=%d hex=%x', n, n) AS resultado
FROM nums;
