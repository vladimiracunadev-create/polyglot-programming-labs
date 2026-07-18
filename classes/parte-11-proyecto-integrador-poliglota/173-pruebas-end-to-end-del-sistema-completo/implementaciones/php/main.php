<?php
[$a, $b, $e] = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "e2e=" . ($a + $b === $e ? "pasa" : "falla") . "\n";
