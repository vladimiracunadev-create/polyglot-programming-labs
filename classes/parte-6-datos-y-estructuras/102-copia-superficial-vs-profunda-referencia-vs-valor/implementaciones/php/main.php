<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
$copia = $nums; // PHP copia los arreglos por valor
$copia[count($copia) - 1] = 99;
echo "original=" . implode("-", $nums) . " copia=" . implode("-", $copia) . "\n";
