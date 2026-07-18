import { readFileSync } from "node:fs";

const n: string = readFileSync(0, "utf8").trim();
console.log(`digitos=${n.length}`);
