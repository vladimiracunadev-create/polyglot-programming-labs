<?php
$t = preg_split('/\s+/', trim(fgets(STDIN)));
if ($t[0] === "cuadrado") {
    $area = (int) $t[1] * (int) $t[1];
} else {
    $area = (int) $t[1] * (int) $t[2];
}
echo "area=$area\n";
