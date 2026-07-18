<?php
$comps = preg_split('/\s+/', trim(fgets(STDIN)));
echo "componentes=" . count($comps) . "\n";
