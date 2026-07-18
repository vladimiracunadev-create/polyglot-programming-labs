<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
echo "contrato=" . ($a === $b ? "compatible" : "incompatible") . "\n";
