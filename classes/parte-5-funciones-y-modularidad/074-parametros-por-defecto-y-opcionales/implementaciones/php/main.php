<?php
function potencia($base, $exp = 2) {
    $r = 1;
    for ($i = 0; $i < $exp; $i++) {
        $r *= $base;
    }
    return $r;
}

$t = preg_split('/\s+/', trim(fgets(STDIN)));
$base = (int) $t[0];
$res = count($t) > 1 ? potencia($base, (int) $t[1]) : potencia($base);
echo "resultado=$res\n";
