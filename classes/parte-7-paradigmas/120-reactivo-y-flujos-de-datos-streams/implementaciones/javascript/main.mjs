import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const stream = nums.filter((x) => x % 2 === 0).map((x) => x * 2);
console.log(`stream=${stream.join("-")}`);
