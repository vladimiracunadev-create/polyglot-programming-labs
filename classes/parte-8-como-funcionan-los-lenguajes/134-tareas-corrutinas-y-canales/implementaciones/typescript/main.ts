import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
let maximo = nums[0];
for (const x of nums) if (x > maximo) maximo = x;
console.log(`max=${maximo}`);
