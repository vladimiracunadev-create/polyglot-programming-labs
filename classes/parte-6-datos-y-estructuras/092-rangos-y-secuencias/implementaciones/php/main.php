<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$r = range((int) $a, (int) $b);
echo "rango=" . implode("-", $r) . " suma=" . array_sum($r) . "\n";
