<?php
$n = (int) trim(fgets(STDIN));
$pares = [];
for ($i = 1; $i <= $n; $i++) {
    $pares[] = 2 * $i;
}
echo "pares=" . implode("-", $pares) . "\n";
