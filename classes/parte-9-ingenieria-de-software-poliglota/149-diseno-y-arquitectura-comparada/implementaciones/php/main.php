<?php
$capas = preg_split('/\s+/', trim(fgets(STDIN)));
echo "capas=" . count($capas) . "\n";
