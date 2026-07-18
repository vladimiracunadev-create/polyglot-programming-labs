<?php
function punto($x, $y) {
    return "punto(x=$x, y=$y)";
}

[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
// PHP 8 admite argumentos nombrados.
echo punto(x: (int) $a, y: (int) $b) . "\n";
