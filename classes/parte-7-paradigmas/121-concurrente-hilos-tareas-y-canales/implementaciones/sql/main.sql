-- SQL: el motor decide el paralelismo; aquí, SUM.
WITH nums(x) AS (VALUES (1), (2), (3), (4))
SELECT printf('suma=%d', sum(x)) AS resultado FROM nums;
