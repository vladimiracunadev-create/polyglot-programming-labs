import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
let recibido = 0;
for (const m of nums) recibido += m;
console.log(`recibido=${recibido}`);
