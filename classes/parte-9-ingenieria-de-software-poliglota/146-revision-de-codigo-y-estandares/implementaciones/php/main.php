<?php
$w = trim(fgets(STDIN));
$valido = preg_match('/^[a-z]+$/', $w) === 1;
echo "valido=" . ($valido ? "true" : "false") . "\n";
