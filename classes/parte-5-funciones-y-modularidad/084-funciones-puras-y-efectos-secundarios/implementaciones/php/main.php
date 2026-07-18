<?php
function cuadrado($n) {
    return $n * $n;
}

$n = (int) trim(fgets(STDIN));
echo "puro=" . cuadrado($n) . "\n";
