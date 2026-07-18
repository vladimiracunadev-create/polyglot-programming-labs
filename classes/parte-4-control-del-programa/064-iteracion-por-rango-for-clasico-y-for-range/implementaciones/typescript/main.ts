import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let f = 1;
for (let i = 1; i <= n; i++) {
  f *= i;
}
console.log(`factorial=${f}`);
