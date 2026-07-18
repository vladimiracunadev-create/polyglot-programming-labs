import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let cuenta = 0;
for (let i = 0; i < n; i++) cuenta += 1;
console.log(`cuenta=${cuenta}`);
