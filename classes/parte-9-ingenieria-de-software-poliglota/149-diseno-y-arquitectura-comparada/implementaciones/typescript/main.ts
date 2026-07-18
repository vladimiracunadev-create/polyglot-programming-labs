import { readFileSync } from "node:fs";

const capas: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`capas=${capas.length}`);
