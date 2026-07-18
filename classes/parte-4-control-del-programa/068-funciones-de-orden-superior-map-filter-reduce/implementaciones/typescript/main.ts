import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const doblados: number[] = nums.map((x) => x * 2);
const total: number = doblados.reduce((a, b) => a + b, 0);
console.log(`doblados=${doblados.join("-")} total=${total}`);
