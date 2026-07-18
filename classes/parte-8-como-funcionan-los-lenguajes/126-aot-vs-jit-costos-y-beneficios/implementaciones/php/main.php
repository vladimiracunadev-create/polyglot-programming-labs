<?php
$n = (int) trim(fgets(STDIN));
$r = 1;
for ($i = 0; $i < $n; $i++) {
    $r *= 2;
}
echo "resultado=$r\n";
