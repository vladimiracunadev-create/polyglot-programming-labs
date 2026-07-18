import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const freq = new Map();
for (const x of nums) freq.set(x, (freq.get(x) || 0) + 1);
console.log(`cuenta=${freq.get(nums[0])}`);
