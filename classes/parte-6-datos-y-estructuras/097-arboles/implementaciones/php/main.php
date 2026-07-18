<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
sort($nums);
echo "inorden=" . implode("-", $nums) . "\n";
