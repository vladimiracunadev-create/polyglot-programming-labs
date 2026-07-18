-- SQL: los conjuntos no comparten referencias mutables; se ilustra el cambio.
WITH nums(pos, x) AS (VALUES (1, 1), (2, 2), (3, 3))
SELECT 'original=' || (SELECT group_concat(x, '-') FROM (SELECT x FROM nums ORDER BY pos))
     || ' copia=' || (SELECT group_concat(CASE WHEN pos = (SELECT max(pos) FROM nums) THEN 99 ELSE x END, '-')
                       FROM (SELECT pos, x FROM nums ORDER BY pos)) AS resultado;
