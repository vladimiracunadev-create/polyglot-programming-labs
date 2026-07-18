import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${(a + b).toFixed(2)} producto=${(a * b).toFixed(2)}`);
