<?php
$n = (int) trim(fgets(STDIN));
$opcion = $n > 0 ? $n : null;
echo $opcion !== null ? "resultado=" . ($opcion * 2) . "\n" : "resultado=nada\n";
