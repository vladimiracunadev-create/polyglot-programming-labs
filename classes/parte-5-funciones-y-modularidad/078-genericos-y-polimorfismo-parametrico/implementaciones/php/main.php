<?php
// PHP es dinámico: la función sirve para cualquier tipo comparable.
function mayor($a, $b) {
    return $a > $b ? $a : $b;
}

[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
echo "max=" . mayor((int) $a, (int) $b) . "\n";
