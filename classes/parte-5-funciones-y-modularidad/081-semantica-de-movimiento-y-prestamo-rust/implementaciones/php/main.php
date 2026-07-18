<?php
$s = trim(fgets(STDIN));
$longitud = strlen($s); // PHP usa GC por conteo de referencias.
echo "movido=$s longitud=$longitud\n";
