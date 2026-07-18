<?php
class Cuenta {
    private $saldo = 0;

    public function depositar($monto) {
        $this->saldo += $monto;
    }

    public function saldo() {
        return $this->saldo;
    }
}

$n = (int) trim(fgets(STDIN));
$c = new Cuenta();
$c->depositar($n);
$c->depositar($n);
echo "saldo=" . $c->saldo() . "\n";
