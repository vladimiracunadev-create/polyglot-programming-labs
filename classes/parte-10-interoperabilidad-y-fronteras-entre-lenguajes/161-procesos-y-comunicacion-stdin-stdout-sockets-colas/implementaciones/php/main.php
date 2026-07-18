<?php
$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
echo "recibido=" . array_sum($nums) . "\n";
