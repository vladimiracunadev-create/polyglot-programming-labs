<?php
$n = (int) trim(fgets(STDIN));
printf("dec=%d hex=%s oct=%s bin=%s\n", $n, dechex($n), decoct($n), decbin($n));
