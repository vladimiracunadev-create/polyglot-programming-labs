<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
echo "divisor=" . ((int) $b % (int) $a === 0 ? "true" : "false") . "\n";
