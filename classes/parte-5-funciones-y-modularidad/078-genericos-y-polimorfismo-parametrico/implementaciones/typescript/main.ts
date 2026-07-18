import { readFileSync } from "node:fs";

function mayor<T>(a: T, b: T): T {
  return a > b ? a : b;
}

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`max=${mayor(a, b)}`);
