<?php
$edad = (int) trim(fgets(STDIN));
if ($edad < 0) {
    echo "invalido\n";
} elseif ($edad < 18) {
    echo "menor\n";
} else {
    echo "adulto\n";
}
