<?php
$n = (int) trim(fgets(STDIN));
$ops = 0;
$suma = 0;
for ($i = 1; $i <= $n; $i++) {
    $suma += $i;
    $ops++;
}
echo "operaciones=$ops resultado=$suma\n";
