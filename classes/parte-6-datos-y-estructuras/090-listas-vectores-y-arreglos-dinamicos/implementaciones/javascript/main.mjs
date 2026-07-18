import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
nums.reverse();
console.log(`invertido=${nums.join("-")}`);
