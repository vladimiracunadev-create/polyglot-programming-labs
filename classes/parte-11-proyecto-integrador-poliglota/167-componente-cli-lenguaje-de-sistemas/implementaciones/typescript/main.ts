import { readFileSync } from "node:fs";

const t: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`comando=${t[0]} args=${t.length - 1}`);
