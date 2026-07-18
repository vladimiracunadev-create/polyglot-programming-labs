-- SQL encapsula con vistas/permisos; aquí el cálculo va en la consulta.
WITH montos(n) AS (VALUES (50), (0), (30))
SELECT printf('saldo=%d', n * 2) AS resultado FROM montos;
