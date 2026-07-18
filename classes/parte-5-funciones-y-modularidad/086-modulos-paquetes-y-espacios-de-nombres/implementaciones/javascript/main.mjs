import { readFileSync } from "node:fs";

// Objeto usado como módulo/espacio de nombres.
const matematicas = {
  doble: (n) => 2 * n,
};

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${matematicas.doble(n)}`);
