<?php
[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$producto = (int) $a * (int) $b;
printf("producto=%d\n", $producto);
