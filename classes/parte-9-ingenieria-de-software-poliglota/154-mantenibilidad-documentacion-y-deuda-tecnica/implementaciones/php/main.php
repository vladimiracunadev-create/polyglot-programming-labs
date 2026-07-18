<?php
$mods = preg_split('/\s+/', trim(fgets(STDIN)));
echo "complejidad=" . count($mods) . "\n";
