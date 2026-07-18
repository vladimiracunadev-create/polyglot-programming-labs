<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
$doblados = array_map(fn($x) => $x * 2, $nums);
echo "doblados=" . implode("-", $doblados) . "\n";
