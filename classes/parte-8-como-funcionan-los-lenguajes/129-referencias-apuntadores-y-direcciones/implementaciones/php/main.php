<?php
$t = preg_split('/\s+/', trim(fgets(STDIN)));
$indice = (int) $t[0];
$lista = array_slice($t, 1);
echo "valor={$lista[$indice]}\n";
