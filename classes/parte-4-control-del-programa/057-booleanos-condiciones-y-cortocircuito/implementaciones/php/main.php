<?php
$n = (int) trim(fgets(STDIN));
$tf = fn($x) => $x ? "true" : "false";
$pos = $n > 0;
$par = $n % 2 === 0;
printf("positivo=%s par=%s ambos=%s\n", $tf($pos), $tf($par), $tf($pos && $par));
