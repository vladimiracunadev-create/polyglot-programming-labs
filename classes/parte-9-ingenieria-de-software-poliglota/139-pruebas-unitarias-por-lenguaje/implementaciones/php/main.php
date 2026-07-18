<?php
[$a, $b, $esperado] = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "test=" . ($a + $b === $esperado ? "pasa" : "falla") . "\n";
