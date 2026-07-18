import { readFileSync } from "node:fs";

function promedio(lista) {
  const suma = lista.reduce((a, b) => a + b, 0);
  return Math.trunc(suma / lista.length);
}

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`promedio=${promedio(nums)}`);
