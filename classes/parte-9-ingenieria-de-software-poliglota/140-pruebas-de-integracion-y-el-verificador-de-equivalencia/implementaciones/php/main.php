<?php
[$x, $y] = preg_split('/\s+/', trim(fgets(STDIN)));
echo "equivalente=" . ($x === $y ? "true" : "false") . "\n";
