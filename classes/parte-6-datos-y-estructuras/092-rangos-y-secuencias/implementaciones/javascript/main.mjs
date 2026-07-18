import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const r = [];
for (let i = a; i <= b; i++) r.push(i);
console.log(`rango=${r.join("-")} suma=${r.reduce((x, y) => x + y, 0)}`);
