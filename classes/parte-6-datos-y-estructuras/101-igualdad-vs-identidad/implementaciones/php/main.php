<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
echo "iguales=" . ((int) $a === (int) $b ? "true" : "false") . "\n";
