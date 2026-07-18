-- SQL: orden descendente (pila) y ascendente (cola) por posición.
WITH nums(pos, x) AS (VALUES (1, 1), (2, 2), (3, 3))
SELECT 'pila=' || (SELECT group_concat(x, '-') FROM (SELECT x FROM nums ORDER BY pos DESC))
     || ' cola=' || (SELECT group_concat(x, '-') FROM (SELECT x FROM nums ORDER BY pos ASC)) AS resultado;
