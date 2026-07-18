import { readFileSync } from "node:fs";

const [estrategia, a, b] = readFileSync(0, "utf8").trim().split(/\s+/);
const x = Number(a), y = Number(b);
const ops: Record<string, number> = { suma: x + y, resta: x - y, producto: x * y };
console.log(`resultado=${ops[estrategia]}`);
