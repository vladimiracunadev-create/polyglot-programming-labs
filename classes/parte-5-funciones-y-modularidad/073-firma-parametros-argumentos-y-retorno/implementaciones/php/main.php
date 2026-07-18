<?php
function suma($a, $b) {
    return $a + $b;
}

[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
echo "suma=" . suma((int) $a, (int) $b) . "\n";
