<?php
$n = (int) trim(fgets(STDIN));
// PHP es síncrono por defecto; se muestra el resultado de la tarea.
echo "resultado=" . ($n * 2) . "\n";
