import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const pares = [];
for (let i = 1; i <= n; i++) pares.push(2 * i);
console.log(`pares=${pares.join("-")}`);
