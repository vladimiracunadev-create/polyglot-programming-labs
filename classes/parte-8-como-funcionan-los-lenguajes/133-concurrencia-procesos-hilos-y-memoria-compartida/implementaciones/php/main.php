<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
$cuenta = 0;
foreach ($nums as $_) {
    $cuenta += 1;
}
echo "cuenta=$cuenta\n";
