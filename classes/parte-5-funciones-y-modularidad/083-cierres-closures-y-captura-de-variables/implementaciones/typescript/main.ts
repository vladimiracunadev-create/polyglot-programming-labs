import { readFileSync } from "node:fs";

function hacerSumador(base: number): (x: number) => number {
  return (x) => base + x;
}

const base: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const sumar = hacerSumador(base);
console.log(`r1=${sumar(1)} r2=${sumar(2)}`);
