<?php
$codigo = (int) trim(fgets(STDIN));
$nombres = [1 => "sintaxis", 2 => "tipos", 3 => "enlace", 4 => "ejecucion"];
echo "error=" . ($nombres[$codigo] ?? "desconocido") . "\n";
