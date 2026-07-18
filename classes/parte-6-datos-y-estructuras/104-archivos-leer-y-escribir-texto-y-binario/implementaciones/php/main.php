<?php
$linea = rtrim(fgets(STDIN), "\r\n");
$palabras = $linea === "" ? 0 : count(preg_split('/\s+/', trim($linea)));
echo "palabras=$palabras caracteres=" . strlen($linea) . "\n";
