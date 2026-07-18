import { readFileSync } from "node:fs";

const actor = { total: 0, recibir(m: number) { this.total += m; } };
const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
for (const m of nums) actor.recibir(m);
console.log(`total=${actor.total}`);
