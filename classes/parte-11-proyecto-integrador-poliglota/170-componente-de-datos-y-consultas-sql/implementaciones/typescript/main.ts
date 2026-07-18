import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`total=${nums.reduce((a, b) => a + b, 0)}`);
