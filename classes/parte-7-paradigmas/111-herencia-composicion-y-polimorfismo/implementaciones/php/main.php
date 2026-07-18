<?php
interface Animal { public function sonido(): string; }
class Perro implements Animal { public function sonido(): string { return "guau"; } }
class Gato implements Animal { public function sonido(): string { return "miau"; } }
class Vaca implements Animal { public function sonido(): string { return "muu"; } }

$tipo = trim(fgets(STDIN));
$animales = ["perro" => new Perro(), "gato" => new Gato(), "vaca" => new Vaca()];
echo "sonido=" . $animales[$tipo]->sonido() . "\n";
