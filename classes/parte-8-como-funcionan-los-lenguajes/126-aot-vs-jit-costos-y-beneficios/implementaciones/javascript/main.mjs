import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let r = 1;
for (let i = 0; i < n; i++) r *= 2;
console.log(`resultado=${r}`);
