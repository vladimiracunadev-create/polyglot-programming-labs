-- SQL: unicode(c) devuelve el punto de código de un carácter.
WITH chars(c) AS (VALUES ('A'), ('z'), ('0'))
SELECT printf('char=%s codigo=%d', c, unicode(c)) AS resultado
FROM chars;
