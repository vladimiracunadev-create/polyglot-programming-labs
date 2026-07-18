import { readFileSync } from "node:fs";

const [x, y]: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
const a: number = parseInt(x, 10);
const b: number = parseFloat(y);
console.log(`suma=${(a + b).toFixed(2)}`);
