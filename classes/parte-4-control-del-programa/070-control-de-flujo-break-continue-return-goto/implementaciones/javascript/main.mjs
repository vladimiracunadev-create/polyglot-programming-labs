import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let d = 2;
for (; d <= n; d++) {
  if (n % d === 0) break;
}
console.log(`primer_divisor=${d}`);
