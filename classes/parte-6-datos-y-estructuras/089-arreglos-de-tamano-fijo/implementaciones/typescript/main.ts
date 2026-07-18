import { readFileSync } from "node:fs";

const arr: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${arr.reduce((a, b) => a + b, 0)} max=${Math.max(...arr)}`);
