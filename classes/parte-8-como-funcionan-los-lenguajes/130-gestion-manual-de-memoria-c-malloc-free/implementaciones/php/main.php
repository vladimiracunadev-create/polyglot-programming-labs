<?php
$n = (int) trim(fgets(STDIN));
$arr = array_fill(0, $n, 0);
for ($i = 0; $i < $n; $i++) {
    $arr[$i] = $i + 1;
}
echo "reservado=$n suma=" . array_sum($arr) . "\n";
