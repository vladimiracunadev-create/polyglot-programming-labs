<?php
interface Forma { public function area(): int; }
class Cuadrado implements Forma {
    public function __construct(private int $l) {}
    public function area(): int { return $this->l * $this->l; }
}
class Rectangulo implements Forma {
    public function __construct(private int $a, private int $b) {}
    public function area(): int { return $this->a * $this->b; }
}

$t = preg_split('/\s+/', trim(fgets(STDIN)));
$f = $t[0] === "cuadrado" ? new Cuadrado((int) $t[1]) : new Rectangulo((int) $t[1], (int) $t[2]);
echo "area=" . $f->area() . "\n";
