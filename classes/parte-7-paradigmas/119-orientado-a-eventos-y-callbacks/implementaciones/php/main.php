<?php
$recolectados = [];
$alEvento = function ($i) use (&$recolectados) {
    $recolectados[] = $i;
};

$n = (int) trim(fgets(STDIN));
for ($i = 1; $i <= $n; $i++) {
    $alEvento($i);
}
echo "eventos=" . implode("-", $recolectados) . "\n";
