-- SQL no modifica variables; el 'despues' se calcula en la expresión.
WITH nums(n) AS (VALUES (5), (3), (7))
SELECT printf('antes=%d despues=%d', n, n * 2) AS resultado FROM nums;
