<?php
$n = (int) trim(fgets(STDIN));
$suma = 0;
$i = 1;
while ($i <= $n) {
    $suma += $i;
    $i++;
}
echo "suma=$suma\n";
