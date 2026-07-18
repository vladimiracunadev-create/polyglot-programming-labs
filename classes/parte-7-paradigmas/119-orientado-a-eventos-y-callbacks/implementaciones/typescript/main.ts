import { readFileSync } from "node:fs";

const recolectados: number[] = [];
const alEvento = (i: number): void => {
  recolectados.push(i);
};

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
for (let i = 1; i <= n; i++) alEvento(i);
console.log(`eventos=${recolectados.join("-")}`);
