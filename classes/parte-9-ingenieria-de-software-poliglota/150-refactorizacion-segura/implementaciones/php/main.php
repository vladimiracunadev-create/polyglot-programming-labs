<?php
$n = (int) trim(fgets(STDIN));
$viejo = $n * 2;
$nuevo = $n + $n;
echo "equivalente=" . ($viejo === $nuevo ? "true" : "false") . " resultado=$nuevo\n";
