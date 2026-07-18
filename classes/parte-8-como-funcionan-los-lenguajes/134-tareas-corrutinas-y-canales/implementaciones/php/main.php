<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "max=" . max($nums) . "\n";
