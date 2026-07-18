<?php
function doblar($x) {
    $x = $x * 2;
    return $x;
}

$n = (int) trim(fgets(STDIN));
$local = doblar($n);
echo "original=$n local=$local\n";
