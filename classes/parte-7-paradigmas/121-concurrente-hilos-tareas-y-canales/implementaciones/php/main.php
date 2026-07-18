<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
$medio = intdiv(count($nums), 2);
$p1 = array_sum(array_slice($nums, 0, $medio));
$p2 = array_sum(array_slice($nums, $medio));
echo "suma=" . ($p1 + $p2) . "\n";
