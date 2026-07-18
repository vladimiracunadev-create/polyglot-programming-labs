-- SQL: WHERE + SUM, puro estilo declarativo.
WITH nums(x) AS (VALUES (1), (2), (3), (4))
SELECT printf('suma_pares=%d', COALESCE(sum(x), 0)) AS resultado FROM nums WHERE x % 2 = 0;
