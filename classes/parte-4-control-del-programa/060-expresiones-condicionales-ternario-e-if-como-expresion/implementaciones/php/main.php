<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $a;
$b = (int) $b;
$mx = $a > $b ? $a : $b;
echo "max=$mx\n";
