import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let ops = 0, suma = 0;
for (let i = 1; i <= n; i++) {
  suma += i;
  ops += 1;
}
console.log(`operaciones=${ops} resultado=${suma}`);
