import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const pares: number[] = [];
for (let i = 1; i <= n; i++) pares.push(2 * i);
console.log(`pares=${pares.join("-")}`);
