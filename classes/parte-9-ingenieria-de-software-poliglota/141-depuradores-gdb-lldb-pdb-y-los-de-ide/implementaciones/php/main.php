<?php
$n = (int) trim(fgets(STDIN));
$acc = 0;
$pasos = [];
for ($i = 1; $i <= $n; $i++) {
    $acc += $i;
    $pasos[] = $acc;
}
echo "traza=" . implode("-", $pasos) . "\n";
