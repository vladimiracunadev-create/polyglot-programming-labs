<?php
function fib($n) {
    return $n < 2 ? $n : fib($n - 1) + fib($n - 2);
}

$n = (int) trim(fgets(STDIN));
echo "fib=" . fib($n) . "\n";
