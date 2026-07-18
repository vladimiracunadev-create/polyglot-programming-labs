<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $a;
$b = (int) $b;
try {
    $r = intdiv($a, $b);
    echo "resultado=$r\n";
} catch (DivisionByZeroError $e) {
    echo "error=division por cero\n";
}
