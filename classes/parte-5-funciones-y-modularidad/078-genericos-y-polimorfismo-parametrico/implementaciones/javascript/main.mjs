import { readFileSync } from "node:fs";

// JS es dinámico: la función ya sirve para cualquier tipo comparable.
function mayor(a, b) {
  return a > b ? a : b;
}

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`max=${mayor(a, b)}`);
