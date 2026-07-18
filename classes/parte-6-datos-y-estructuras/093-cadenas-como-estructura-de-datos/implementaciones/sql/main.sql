-- SQL: sqlite no trae reverse; se invierte con un CTE recursivo (ilustrativo).
WITH RECURSIVE r(i, acc, s) AS (
    SELECT length('hola'), '', 'hola'
    UNION ALL SELECT i - 1, acc || substr(s, i, 1), s FROM r WHERE i > 0
)
SELECT 'invertido=' || acc AS resultado FROM r WHERE i = 0;
