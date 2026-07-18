<?php
$msgs = preg_split('/\s+/', trim(fgets(STDIN)));
echo "commits=" . count($msgs) . "\n";
