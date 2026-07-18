import { readFileSync } from "node:fs";

function divmod(a: number, b: number): [number, number] {
  return [Math.trunc(a / b), a % b];
}

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const [q, r]: [number, number] = divmod(a, b);
console.log(`cociente=${q} resto=${r}`);
