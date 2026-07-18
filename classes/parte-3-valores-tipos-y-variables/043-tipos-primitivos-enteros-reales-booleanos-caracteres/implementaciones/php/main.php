<?php
$n = (int) trim(fgets(STDIN));
$par = ($n % 2 === 0) ? "true" : "false";
printf("entero=%d real=%.1f par=%s\n", $n, (float) $n, $par);
