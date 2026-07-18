<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
$stream = array_map(fn($x) => $x * 2, array_filter($nums, fn($x) => $x % 2 === 0));
echo "stream=" . implode("-", $stream) . "\n";
