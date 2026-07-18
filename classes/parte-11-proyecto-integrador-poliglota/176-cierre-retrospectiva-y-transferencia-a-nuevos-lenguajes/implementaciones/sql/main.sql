-- SQL, la ultima vez: la misma idea, otra forma.
WITH t(n) AS (VALUES (5))
SELECT printf('lecciones=%d transferible=si', n) AS resultado FROM t;
