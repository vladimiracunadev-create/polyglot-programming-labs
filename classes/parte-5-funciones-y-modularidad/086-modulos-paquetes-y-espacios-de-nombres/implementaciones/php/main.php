<?php
// PHP usa namespaces; aquí una función que actúa como utilidad del módulo.
function matematicas_doble($n) {
    return 2 * $n;
}

$n = (int) trim(fgets(STDIN));
echo "resultado=" . matematicas_doble($n) . "\n";
