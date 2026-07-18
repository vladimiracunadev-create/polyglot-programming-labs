import { readFileSync } from "node:fs";

function sumar(n) {
  return n === 0 ? 0 : n + sumar(n - 1);
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`suma=${sumar(n)} profundidad=${n}`);
