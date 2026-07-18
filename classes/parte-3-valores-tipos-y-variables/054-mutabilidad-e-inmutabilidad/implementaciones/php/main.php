<?php
$n = (int) trim(fgets(STDIN));
$parts = [];
for ($i = 1; $i <= $n; $i++) {
    $parts[] = $i;
}
echo "sec=" . implode("-", $parts) . "\n";
