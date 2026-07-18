import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`checksum=${nums.reduce((a, b) => a + b, 0)}`);
