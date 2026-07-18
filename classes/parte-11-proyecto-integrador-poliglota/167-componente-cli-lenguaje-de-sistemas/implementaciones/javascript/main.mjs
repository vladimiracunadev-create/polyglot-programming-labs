import { readFileSync } from "node:fs";

const t = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`comando=${t[0]} args=${t.length - 1}`);
