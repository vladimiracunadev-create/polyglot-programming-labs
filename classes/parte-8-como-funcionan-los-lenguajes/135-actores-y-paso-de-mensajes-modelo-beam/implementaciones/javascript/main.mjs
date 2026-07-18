import { readFileSync } from "node:fs";

const actor = { total: 0, recibir(m) { this.total += m; } };
const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
for (const m of nums) actor.recibir(m);
console.log(`total=${actor.total}`);
