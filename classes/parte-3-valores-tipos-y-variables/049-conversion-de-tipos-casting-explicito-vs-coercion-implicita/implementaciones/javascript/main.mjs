import { readFileSync } from "node:fs";

const f = parseFloat(readFileSync(0, "utf8").trim());
console.log(`entero=${Math.trunc(f)} real=${f.toFixed(2)}`);
