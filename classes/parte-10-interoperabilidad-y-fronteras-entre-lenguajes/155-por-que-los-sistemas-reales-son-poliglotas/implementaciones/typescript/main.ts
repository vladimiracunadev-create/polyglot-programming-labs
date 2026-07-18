import { readFileSync } from "node:fs";

const comps: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`componentes=${comps.length}`);
