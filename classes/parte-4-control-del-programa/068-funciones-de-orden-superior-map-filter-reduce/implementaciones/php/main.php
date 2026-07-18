<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$doblados = array_map(fn($x) => (int) $x * 2, $nums);
$total = array_reduce($doblados, fn($a, $b) => $a + $b, 0);
echo "doblados=" . implode("-", $doblados) . " total=$total\n";
