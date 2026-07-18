import { readFileSync } from "node:fs";

const t = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const indice = t[0];
const lista = t.slice(1);
console.log(`valor=${lista[indice]}`);
