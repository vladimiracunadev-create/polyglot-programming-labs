<?php
[$clave, $valor] = preg_split('/\s+/', trim(fgets(STDIN)));
$almacen = [];
$almacen[$clave] = $valor;
echo "guardado=$clave={$almacen[$clave]}\n";
