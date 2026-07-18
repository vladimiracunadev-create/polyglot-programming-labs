<?php
class Recurso {
    public function __construct(public int $valor) {}
    public function __destruct() { /* se libera aquí */ }
}

$n = (int) trim(fgets(STDIN));
$r = new Recurso($n);
$valor = $r->valor;
unset($r); // libera el recurso
echo "valor=$valor estado=liberado\n";
