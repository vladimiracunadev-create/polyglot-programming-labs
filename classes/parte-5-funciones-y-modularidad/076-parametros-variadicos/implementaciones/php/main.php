<?php
function suma(...$nums) {
    return array_sum($nums);
}

$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "suma=" . suma(...$nums) . "\n";
