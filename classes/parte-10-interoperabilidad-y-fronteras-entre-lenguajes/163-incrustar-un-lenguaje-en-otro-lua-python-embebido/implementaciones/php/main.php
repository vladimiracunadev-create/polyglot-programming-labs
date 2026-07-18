<?php
[$a, $b] = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "resultado=" . ($a + $b) . "\n";
