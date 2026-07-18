import { readFileSync } from "node:fs";

function cuadrado(n) {
  return n * n;
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`puro=${cuadrado(n)}`);
