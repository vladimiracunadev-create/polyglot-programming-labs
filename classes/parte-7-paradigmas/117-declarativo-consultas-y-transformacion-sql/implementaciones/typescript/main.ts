import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const suma = nums.filter((x) => x % 2 === 0).reduce((a, b) => a + b, 0);
console.log(`suma_pares=${suma}`);
