import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let suma = 0;
let i = 1;
while (i <= n) {
  suma += i;
  i++;
}
console.log(`suma=${suma}`);
