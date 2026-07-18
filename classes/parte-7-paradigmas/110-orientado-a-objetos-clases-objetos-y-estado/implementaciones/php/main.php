<?php
class Contador {
    public int $cuenta = 0;
    public function incrementar() {
        $this->cuenta++;
    }
}

$n = (int) trim(fgets(STDIN));
$c = new Contador();
for ($i = 0; $i < $n; $i++) {
    $c->incrementar();
}
echo "cuenta={$c->cuenta}\n";
