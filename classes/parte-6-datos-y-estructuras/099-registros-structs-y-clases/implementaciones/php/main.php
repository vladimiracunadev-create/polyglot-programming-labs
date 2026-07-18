<?php
class Persona {
    public function __construct(public string $nombre, public int $edad) {}
}

$t = preg_split('/\s+/', trim(fgets(STDIN)));
$p = new Persona($t[0], (int) $t[1]);
echo "Persona(nombre={$p->nombre}, edad={$p->edad})\n";
