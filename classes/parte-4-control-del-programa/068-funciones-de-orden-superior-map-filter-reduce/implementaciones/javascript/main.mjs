import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const doblados = nums.map((x) => x * 2);
const total = doblados.reduce((a, b) => a + b, 0);
console.log(`doblados=${doblados.join("-")} total=${total}`);
