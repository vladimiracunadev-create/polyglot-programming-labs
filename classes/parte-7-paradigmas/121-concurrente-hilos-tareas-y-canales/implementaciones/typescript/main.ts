import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const medio = Math.floor(nums.length / 2);
const p1 = nums.slice(0, medio).reduce((a, b) => a + b, 0);
const p2 = nums.slice(medio).reduce((a, b) => a + b, 0);
console.log(`suma=${p1 + p2}`);
