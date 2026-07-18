import { readFileSync } from "node:fs";

function doblar(x) {
  x = x * 2;
  return x;
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const local = doblar(n);
console.log(`original=${n} local=${local}`);
