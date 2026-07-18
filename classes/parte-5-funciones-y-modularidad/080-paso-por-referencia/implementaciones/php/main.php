<?php
function doblar(&$x) {
    $x *= 2;
}

$n = (int) trim(fgets(STDIN));
$antes = $n;
doblar($n);
echo "antes=$antes despues=$n\n";
