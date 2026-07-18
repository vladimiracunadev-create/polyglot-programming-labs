<?php
$suma = fn($a, $b) => $a + $b;
$producto = fn($a, $b) => $a * $b;
function aplicar($f, $a, $b) {
    return $f($a, $b);
}

[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $a;
$b = (int) $b;
echo "suma=" . aplicar($suma, $a, $b) . " producto=" . aplicar($producto, $a, $b) . "\n";
