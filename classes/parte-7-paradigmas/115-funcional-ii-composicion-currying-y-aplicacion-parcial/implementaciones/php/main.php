<?php
$doblar = fn($x) => $x * 2;
$incrementar = fn($x) => $x + 1;
$compuesta = fn($x) => $incrementar($doblar($x));

$n = (int) trim(fgets(STDIN));
echo "resultado=" . $compuesta($n) . "\n";
