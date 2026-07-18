import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const pares: number[] = nums.filter((x) => x % 2 === 0);
console.log(`pares=${pares.join("-")}`);
