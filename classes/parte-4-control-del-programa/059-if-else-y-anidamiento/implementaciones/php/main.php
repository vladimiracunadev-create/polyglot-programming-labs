<?php
$score = (int) trim(fgets(STDIN));
if ($score >= 90) {
    $nota = "A";
} elseif ($score >= 80) {
    $nota = "B";
} elseif ($score >= 70) {
    $nota = "C";
} else {
    $nota = "F";
}
echo "nota=$nota\n";
