-- SQL: rangos con CASE WHEN en orden descendente.
WITH scores(score) AS (VALUES (95), (72), (40))
SELECT printf('nota=%s',
       CASE WHEN score >= 90 THEN 'A'
            WHEN score >= 80 THEN 'B'
            WHEN score >= 70 THEN 'C'
            ELSE 'F' END) AS resultado
FROM scores;
