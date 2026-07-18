<?php
function divmod($a, $b) {
    return [intdiv($a, $b), $a % $b];
}

[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
[$q, $r] = divmod((int) $a, (int) $b);
echo "cociente=$q resto=$r\n";
