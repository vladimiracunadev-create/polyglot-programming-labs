<?php
$pasos = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
$verde = !in_array(0, $pasos, true);
echo "ci=" . ($verde ? "verde" : "rojo") . "\n";
