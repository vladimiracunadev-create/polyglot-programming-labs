<?php
[$x, $y] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $x;
$b = (float) $y;
printf("suma=%.2f\n", $a + $b);
