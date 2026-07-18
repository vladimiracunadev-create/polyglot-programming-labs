-- SQL es declarativo: no lee stdin como los lenguajes imperativos. En vez de
-- una variable que se asigna, se describe el cálculo sobre una tabla de valores.
-- Esta consulta demuestra la misma fórmula para los tres casos de casos.json.
WITH ventas(precio_unitario, cantidad, descuento) AS (
    VALUES (15000.0, 2, 0.10),
           (999.9, 3, 0.0),
           (5000.0, 0, 0.20)
)
SELECT printf('Total: %.2f', precio_unitario * cantidad * (1 - descuento)) AS resultado
FROM ventas;
