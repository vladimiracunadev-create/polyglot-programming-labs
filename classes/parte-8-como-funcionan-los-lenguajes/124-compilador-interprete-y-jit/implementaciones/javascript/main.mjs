import { readFileSync } from "node:fs";

const n = readFileSync(0, "utf8").trim();
console.log(`digitos=${n.length}`);
