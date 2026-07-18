import { readFileSync } from "node:fs";

const [x, y] = readFileSync(0, "utf8").trim().split(/\s+/);
const a = parseInt(x, 10);
const b = parseFloat(y);
console.log(`suma=${(a + b).toFixed(2)}`);
