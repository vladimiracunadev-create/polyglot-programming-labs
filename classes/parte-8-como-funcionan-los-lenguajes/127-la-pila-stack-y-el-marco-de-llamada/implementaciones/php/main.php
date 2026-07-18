<?php
function sumar($n) {
    return $n === 0 ? 0 : $n + sumar($n - 1);
}

$n = (int) trim(fgets(STDIN));
echo "suma=" . sumar($n) . " profundidad=$n\n";
