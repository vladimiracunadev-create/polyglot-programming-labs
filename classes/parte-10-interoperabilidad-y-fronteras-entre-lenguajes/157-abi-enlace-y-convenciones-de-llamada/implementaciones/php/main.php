<?php
[$a, $b] = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "abi=" . ($a === $b ? "compatible" : "incompatible") . "\n";
