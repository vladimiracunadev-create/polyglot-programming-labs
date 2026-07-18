-- SQL concatena con || (no con +).
WITH nums(n) AS (VALUES (5), (3), (12))
SELECT printf('suma=%d texto=%s', n + n, n || n) AS resultado
FROM nums;
