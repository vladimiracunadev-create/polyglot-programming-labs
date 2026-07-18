<?php
$n = (int) trim(fgets(STDIN));
$f = 1;
for ($i = 1; $i <= $n; $i++) {
    $f *= $i;
}
echo "factorial=$f\n";
