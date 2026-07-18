<?php
function doble($x) { return $x * 2; }
function wrapper($x) { return "wrap(" . doble($x) . ")"; }

$n = (int) trim(fgets(STDIN));
echo "envuelto=" . wrapper($n) . "\n";
