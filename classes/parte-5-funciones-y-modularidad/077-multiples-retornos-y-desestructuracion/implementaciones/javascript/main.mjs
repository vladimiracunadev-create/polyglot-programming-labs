import { readFileSync } from "node:fs";

function divmod(a, b) {
  return [Math.trunc(a / b), a % b];
}

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const [q, r] = divmod(a, b);
console.log(`cociente=${q} resto=${r}`);
