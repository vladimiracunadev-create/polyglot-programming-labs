<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$aristas = intdiv(count($nums), 2);
$nodos = count(array_unique($nums));
echo "aristas=$aristas nodos=$nodos\n";
