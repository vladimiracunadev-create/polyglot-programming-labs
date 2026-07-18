<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$a = ((int) $a) !== 0;
$b = ((int) $b) !== 0;
$tf = fn($x) => $x ? "true" : "false";
printf("and=%s or=%s not_a=%s\n", $tf($a && $b), $tf($a || $b), $tf(!$a));
