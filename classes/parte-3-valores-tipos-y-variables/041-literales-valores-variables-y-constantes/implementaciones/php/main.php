<?php
// PHP: dinámico y débilmente tipado; las variables llevan el prefijo $.
$linea = trim(fgets(STDIN));
[$precio, $cantidad, $descuento] = preg_split('/\s+/', $linea);

$precioUnitario = (float) $precio;
$cantidadInt = (int) $cantidad;
$descuentoFloat = (float) $descuento;

$subtotal = $precioUnitario * $cantidadInt;
$total = $subtotal * (1 - $descuentoFloat);

printf("Total: %.2f\n", $total);
