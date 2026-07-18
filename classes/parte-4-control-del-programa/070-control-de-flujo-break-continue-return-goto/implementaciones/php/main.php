<?php
$n = (int) trim(fgets(STDIN));
$d = 2;
for (; $d <= $n; $d++) {
    if ($n % $d === 0) {
        break;
    }
}
echo "primer_divisor=$d\n";
