import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
nums.sort((a, b) => a - b);
console.log(`inorden=${nums.join("-")}`);
