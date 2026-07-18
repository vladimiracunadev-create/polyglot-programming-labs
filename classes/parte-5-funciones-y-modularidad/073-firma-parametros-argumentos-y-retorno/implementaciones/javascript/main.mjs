import { readFileSync } from "node:fs";

function suma(a, b) {
  return a + b;
}

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${suma(a, b)}`);
