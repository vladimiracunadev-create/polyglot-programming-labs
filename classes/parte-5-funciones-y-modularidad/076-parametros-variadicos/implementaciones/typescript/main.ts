import { readFileSync } from "node:fs";

function suma(...nums: number[]): number {
  return nums.reduce((a, b) => a + b, 0);
}

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${suma(...nums)}`);
