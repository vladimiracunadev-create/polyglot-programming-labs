import { readFileSync } from "node:fs";

const [a, b, op] = readFileSync(0, "utf8").trim().split(/\s+/);
const pila = [Number(a), Number(b)];
const y = pila.pop(), x = pila.pop();
const r = op === "+" ? x + y : op === "-" ? x - y : x * y;
console.log(`resultado=${r}`);
