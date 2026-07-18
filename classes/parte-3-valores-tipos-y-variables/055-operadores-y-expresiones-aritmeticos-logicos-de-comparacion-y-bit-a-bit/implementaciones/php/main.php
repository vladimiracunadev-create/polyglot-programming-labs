<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = (int) $a;
$b = (int) $b;
printf("suma=%d resta=%d mult=%d div=%d mod=%d\n", $a + $b, $a - $b, $a * $b, intdiv($a, $b), $a % $b);
