<?php
function dividir($a, $b) {
    if ($b === 0) {
        return ["err" => "division"];
    }
    return ["ok" => intdiv($a, $b)];
}

[$a, $b] = preg_split('/\s+/', trim(fgets(STDIN)));
$r = dividir((int) $a, (int) $b);
echo isset($r["err"]) ? "err={$r['err']}\n" : "ok={$r['ok']}\n";
