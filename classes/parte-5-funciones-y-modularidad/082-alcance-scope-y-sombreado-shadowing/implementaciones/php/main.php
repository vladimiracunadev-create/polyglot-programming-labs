<?php
$n = (int) trim(fgets(STDIN));
$x = $n;
// PHP no tiene alcance de bloque: se usa otra variable.
$xInterno = $x + 10;
echo "interno=$xInterno externo=$x\n";
