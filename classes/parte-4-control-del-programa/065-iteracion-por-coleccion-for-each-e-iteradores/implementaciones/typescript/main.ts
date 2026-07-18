import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
let suma = 0;
for (const x of nums) {
  suma += x;
}
console.log(`suma=${suma}`);
