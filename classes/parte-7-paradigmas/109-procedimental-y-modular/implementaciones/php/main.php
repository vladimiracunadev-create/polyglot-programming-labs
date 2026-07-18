<?php
function promedio($a) {
    return intdiv(array_sum($a), count($a));
}

$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "promedio=" . promedio($nums) . "\n";
