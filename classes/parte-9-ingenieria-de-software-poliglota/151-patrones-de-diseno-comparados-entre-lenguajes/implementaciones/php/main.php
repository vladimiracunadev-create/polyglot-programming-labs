<?php
[$e, $a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $a;
$b = (int) $b;
$ops = ["suma" => $a + $b, "resta" => $a - $b, "producto" => $a * $b];
echo "resultado=" . $ops[$e] . "\n";
