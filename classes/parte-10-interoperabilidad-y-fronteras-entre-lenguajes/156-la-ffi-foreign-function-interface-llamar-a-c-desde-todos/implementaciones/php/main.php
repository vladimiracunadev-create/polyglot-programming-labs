<?php
function doble($x) { return $x * 2; } // simula una extension en C

$n = (int) trim(fgets(STDIN));
echo "resultado=" . doble($n) . "\n";
