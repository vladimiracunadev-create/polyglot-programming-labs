<?php
$t = preg_split('/\s+/', trim(fgets(STDIN)));
echo "comando={$t[0]} args=" . (count($t) - 1) . "\n";
