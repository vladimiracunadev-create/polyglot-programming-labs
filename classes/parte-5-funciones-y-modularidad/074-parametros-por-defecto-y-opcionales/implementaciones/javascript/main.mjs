import { readFileSync } from "node:fs";

function potencia(base, exp = 2) {
  let r = 1;
  for (let i = 0; i < exp; i++) r *= base;
  return r;
}

const t = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`resultado=${t.length > 1 ? potencia(t[0], t[1]) : potencia(t[0])}`);
