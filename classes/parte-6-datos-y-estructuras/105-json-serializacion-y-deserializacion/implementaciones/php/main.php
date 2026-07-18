<?php
$t = preg_split('/\s+/', trim(fgets(STDIN)));
$nombre = $t[0];
$edad = (int) $t[1];
echo "{\"nombre\": \"$nombre\", \"edad\": $edad}\n";
