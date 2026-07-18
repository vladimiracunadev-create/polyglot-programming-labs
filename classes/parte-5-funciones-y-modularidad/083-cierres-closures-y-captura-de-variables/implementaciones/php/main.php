<?php
function hacerSumador($base) {
    return fn($x) => $base + $x;
}

$base = (int) trim(fgets(STDIN));
$sumar = hacerSumador($base);
echo "r1=" . $sumar(1) . " r2=" . $sumar(2) . "\n";
