-- SQL: separa la versión con funciones de texto (ilustrativo).
WITH v(s) AS (VALUES ('1.2.3'))
SELECT printf('mayor=%d menor=%d parche=%d',
       CAST(substr(s, 1, instr(s, '.') - 1) AS INTEGER),
       CAST(substr(s, instr(s, '.') + 1, instr(substr(s, instr(s, '.') + 1), '.') - 1) AS INTEGER),
       CAST(substr(s, length(s) - instr(reverse(s), '.') + 2) AS INTEGER)) AS resultado
FROM v;
