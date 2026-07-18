<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$pares = array_filter($nums, fn($x) => (int) $x % 2 === 0);
echo "pares=" . implode("-", $pares) . "\n";
