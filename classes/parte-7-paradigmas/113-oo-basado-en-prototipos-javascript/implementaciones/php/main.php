<?php
$n = (int) trim(fgets(STDIN));
$obj = new class($n) {
    public function __construct(public int $valor) {}
    public function doble(): int { return $this->valor * 2; }
};
echo "resultado=" . $obj->doble() . "\n";
