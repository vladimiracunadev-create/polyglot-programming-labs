import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`suma=${n + n} texto=${String(n) + String(n)}`);
