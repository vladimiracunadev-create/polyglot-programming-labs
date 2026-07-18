<?php
[$a, $b, $c] = preg_split('/\s+/', trim(fgets(STDIN)));
$arr = [(int) $a, (int) $b, (int) $c];
echo "suma=" . array_sum($arr) . " max=" . max($arr) . "\n";
