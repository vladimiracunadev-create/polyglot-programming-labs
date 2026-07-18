import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let acc = 0;
const pasos = [];
for (let i = 1; i <= n; i++) {
  acc += i;
  pasos.push(acc);
}
console.log(`traza=${pasos.join("-")}`);
