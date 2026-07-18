import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let suma = 0;
for (let i = 1; i <= n; i++) suma += i;
console.log(`suma=${suma}`);
