<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "checksum=" . array_sum($nums) . "\n";
