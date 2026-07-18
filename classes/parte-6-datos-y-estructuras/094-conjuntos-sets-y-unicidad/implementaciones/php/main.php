<?php
$nums = preg_split('/\s+/', trim(fgets(STDIN)));
echo "unicos=" . count(array_unique($nums)) . "\n";
