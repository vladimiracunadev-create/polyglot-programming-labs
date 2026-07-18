-- SQL: cuenta las filas (commits).
WITH commits(msg) AS (VALUES ('fix'), ('add'), ('refactor'))
SELECT printf('commits=%d', count(*)) AS resultado FROM commits;
