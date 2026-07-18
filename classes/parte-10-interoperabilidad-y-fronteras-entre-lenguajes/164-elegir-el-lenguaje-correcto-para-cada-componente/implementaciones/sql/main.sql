-- SQL recomienda con CASE.
WITH t(tipo) AS (VALUES ('sistemas'))
SELECT printf('lenguaje=%s', CASE tipo WHEN 'sistemas' THEN 'Rust' WHEN 'web' THEN 'TypeScript' WHEN 'datos' THEN 'SQL' ELSE 'Python' END) AS resultado FROM t;
