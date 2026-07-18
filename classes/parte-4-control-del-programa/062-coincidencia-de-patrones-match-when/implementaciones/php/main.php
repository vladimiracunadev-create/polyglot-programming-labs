<?php
$n = (int) trim(fgets(STDIN));
$signo = match (true) {
    $n > 0 => "positivo",
    $n < 0 => "negativo",
    default => "cero",
};
echo "signo=$signo\n";
