import { readFileSync } from "node:fs";

function doblar(x: number): number {
  x = x * 2;
  return x;
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const local: number = doblar(n);
console.log(`original=${n} local=${local}`);
