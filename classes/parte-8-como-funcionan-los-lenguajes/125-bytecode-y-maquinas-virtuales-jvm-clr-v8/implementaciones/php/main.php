<?php
[$a, $b, $op] = preg_split('/\s+/', trim(fgets(STDIN)));
$pila = [(int) $a, (int) $b];
$y = array_pop($pila);
$x = array_pop($pila);
$r = $op === "+" ? $x + $y : ($op === "-" ? $x - $y : $x * $y);
echo "resultado=$r\n";
