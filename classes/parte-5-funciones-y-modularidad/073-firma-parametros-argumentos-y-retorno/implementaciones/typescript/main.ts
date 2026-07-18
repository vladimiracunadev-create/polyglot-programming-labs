import { readFileSync } from "node:fs";

function suma(a: number, b: number): number {
  return a + b;
}

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${suma(a, b)}`);
