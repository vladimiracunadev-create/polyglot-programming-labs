import { readFileSync } from "node:fs";

function potencia(base: number, exp = 2): number {
  let r = 1;
  for (let i = 0; i < exp; i++) r *= base;
  return r;
}

const t: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`resultado=${t.length > 1 ? potencia(t[0], t[1]) : potencia(t[0])}`);
