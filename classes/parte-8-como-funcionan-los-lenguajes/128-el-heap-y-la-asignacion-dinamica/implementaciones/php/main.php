<?php
$n = (int) trim(fgets(STDIN));
$lista = [];
for ($i = $n; $i >= 1; $i--) {
    $lista[] = $i;
}
echo "lista=" . implode("-", $lista) . "\n";
