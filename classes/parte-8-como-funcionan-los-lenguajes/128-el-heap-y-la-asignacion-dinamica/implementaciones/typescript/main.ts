import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const lista: number[] = [];
for (let i = n; i >= 1; i--) lista.push(i);
console.log(`lista=${lista.join("-")}`);
