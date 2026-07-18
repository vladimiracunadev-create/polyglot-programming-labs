-- SQL no expone la gestión de memoria; se calcula la suma.
WITH RECURSIVE r(i) AS (VALUES (1) UNION ALL SELECT i + 1 FROM r WHERE i < 5)
SELECT printf('reservado=%d suma=%d', max(i), sum(i)) AS resultado FROM r;
