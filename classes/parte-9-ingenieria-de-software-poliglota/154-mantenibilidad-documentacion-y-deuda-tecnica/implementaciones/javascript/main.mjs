import { readFileSync } from "node:fs";

const mods = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`complejidad=${mods.length}`);
