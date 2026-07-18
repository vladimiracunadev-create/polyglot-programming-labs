-- SQL: length sobre el texto del número.
WITH nums(n) AS (VALUES ('12345'))
SELECT printf('digitos=%d', length(n)) AS resultado FROM nums;
