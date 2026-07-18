<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$pila = implode("-", array_reverse($nums));
$cola = implode("-", $nums);
echo "pila=$pila cola=$cola\n";
