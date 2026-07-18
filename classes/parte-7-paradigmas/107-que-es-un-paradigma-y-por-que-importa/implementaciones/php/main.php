<?php
$n = (int) trim(fgets(STDIN));
$suma = 0;
for ($i = 1; $i <= $n; $i++) {
    $suma += $i;
}
echo "suma=$suma\n";
