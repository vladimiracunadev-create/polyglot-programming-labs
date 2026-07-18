import { readFileSync } from "node:fs";

function cuadrado(n: number): number {
  return n * n;
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`puro=${cuadrado(n)}`);
