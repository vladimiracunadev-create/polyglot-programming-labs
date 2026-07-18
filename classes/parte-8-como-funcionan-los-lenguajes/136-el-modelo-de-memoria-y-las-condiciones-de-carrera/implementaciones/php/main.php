<?php
$n = (int) trim(fgets(STDIN));
$cuenta = 0;
for ($i = 0; $i < $n; $i++) {
    $cuenta += 1;
}
echo "cuenta=$cuenta\n";
