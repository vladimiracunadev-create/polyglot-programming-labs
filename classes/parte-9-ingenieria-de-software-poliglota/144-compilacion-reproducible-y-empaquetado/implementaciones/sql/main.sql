-- SQL: SUM como checksum simple.
WITH nums(x) AS (VALUES (1), (2), (3))
SELECT printf('checksum=%d', sum(x)) AS resultado FROM nums;
