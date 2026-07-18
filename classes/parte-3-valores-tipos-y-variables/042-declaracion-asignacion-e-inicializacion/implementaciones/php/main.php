<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $a;
$b = (int) $b;

// PHP admite intercambio por lista.
[$a, $b] = [$b, $a];

printf("a=%d b=%d\n", $a, $b);
