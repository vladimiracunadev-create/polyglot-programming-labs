<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (float) $a;
$b = (float) $b;
printf("suma=%.2f producto=%.2f\n", $a + $b, $a * $b);
