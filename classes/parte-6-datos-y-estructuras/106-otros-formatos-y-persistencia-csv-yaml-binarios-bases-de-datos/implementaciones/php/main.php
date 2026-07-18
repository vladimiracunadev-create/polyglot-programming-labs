<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
echo "csv=" . implode(",", $nums) . " campos=" . count($nums) . "\n";
