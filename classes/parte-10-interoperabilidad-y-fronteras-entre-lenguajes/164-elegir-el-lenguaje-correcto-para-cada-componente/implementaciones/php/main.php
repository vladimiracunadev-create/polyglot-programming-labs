<?php
$tipo = trim(fgets(STDIN));
$rec = ["sistemas" => "Rust", "web" => "TypeScript", "datos" => "SQL"];
echo "lenguaje=" . ($rec[$tipo] ?? "Python") . "\n";
