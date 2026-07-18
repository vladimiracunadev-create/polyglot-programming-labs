import { readFileSync } from "node:fs";

const recolectados = [];
const alEvento = (i) => recolectados.push(i);

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
for (let i = 1; i <= n; i++) alEvento(i);
console.log(`eventos=${recolectados.join("-")}`);
