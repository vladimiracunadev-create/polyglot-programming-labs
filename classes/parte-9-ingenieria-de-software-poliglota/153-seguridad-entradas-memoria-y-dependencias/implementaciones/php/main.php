<?php
$w = trim(fgets(STDIN));
$seguro = ctype_alnum($w);
echo "seguro=" . ($seguro ? "true" : "false") . "\n";
