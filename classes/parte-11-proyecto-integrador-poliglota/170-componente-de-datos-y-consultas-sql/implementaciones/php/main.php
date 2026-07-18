<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "total=" . array_sum($nums) . "\n";
