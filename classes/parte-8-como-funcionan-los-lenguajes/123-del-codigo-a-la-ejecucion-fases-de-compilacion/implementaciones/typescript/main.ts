import { readFileSync } from "node:fs";

const [a, op, b] = readFileSync(0, "utf8").trim().split(/\s+/);
const x = Number(a), y = Number(b);
const r = op === "+" ? x + y : op === "-" ? x - y : x * y;
console.log(`resultado=${r}`);
