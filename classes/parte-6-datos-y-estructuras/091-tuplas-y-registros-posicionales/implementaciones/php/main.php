<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$t = [(int) $b, (int) $a];
echo "tupla=({$t[0]}, {$t[1]})\n";
