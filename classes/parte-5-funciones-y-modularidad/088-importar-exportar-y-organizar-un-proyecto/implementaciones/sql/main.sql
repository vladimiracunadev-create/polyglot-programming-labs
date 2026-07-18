-- SQL: abs() incorporado.
WITH nums(n) AS (VALUES (-5), (3), (0))
SELECT printf('abs=%d', abs(n)) AS resultado FROM nums;
