<?php
function doble($x) {
    return $x * 2;
}

$n = (int) trim(fgets(STDIN));
echo "resultado=" . doble($n) . "\n";
