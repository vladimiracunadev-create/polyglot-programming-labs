import { readFileSync } from "node:fs";

const mods: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`complejidad=${mods.length}`);
