<?php
$n = (int) trim(fgets(STDIN));
for ($i = 0; $i < $n; $i++) {
    $tmp = new stdClass(); // recolectado por conteo de referencias
    unset($tmp);
}
echo "creados=$n estado=recolectado\n";
