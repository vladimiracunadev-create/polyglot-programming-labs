<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$nums = array_reverse($nums);
echo "invertido=" . implode("-", $nums) . "\n";
