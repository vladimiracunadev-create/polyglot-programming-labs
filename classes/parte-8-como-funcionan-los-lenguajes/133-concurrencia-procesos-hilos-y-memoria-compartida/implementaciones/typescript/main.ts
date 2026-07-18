import { readFileSync } from "node:fs";

const nums: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
let cuenta = 0;
for (const _ of nums) cuenta += 1;
console.log(`cuenta=${cuenta}`);
