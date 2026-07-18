<?php
$c = preg_split('/\s+/', trim(fgets(STDIN)));
echo "componentes=" . count($c) . " nombres=" . implode("-", $c) . "\n";
