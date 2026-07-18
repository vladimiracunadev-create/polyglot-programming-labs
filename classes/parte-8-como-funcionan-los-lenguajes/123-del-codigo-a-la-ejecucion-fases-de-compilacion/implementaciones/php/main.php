<?php
[$a, $op, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $a;
$b = (int) $b;
$r = $op === "+" ? $a + $b : ($op === "-" ? $a - $b : $a * $b);
echo "resultado=$r\n";
