<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
$suma = array_sum(array_filter($nums, fn($x) => $x % 2 === 0));
echo "suma_pares=$suma\n";
