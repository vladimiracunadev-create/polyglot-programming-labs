<?php
class Acumulador {
    public int $total = 0;
    public function recibir($m) { $this->total += $m; }
}

$nums = array_map('intval', preg_split('/\s+/', trim(fgets(STDIN))));
$actor = new Acumulador();
foreach ($nums as $m) {
    $actor->recibir($m);
}
echo "total={$actor->total}\n";
