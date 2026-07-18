<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
$freq = array_count_values($nums);
echo "cuenta=" . $freq[$nums[0]] . "\n";
