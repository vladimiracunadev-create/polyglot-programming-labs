import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const pares = nums.filter((x) => x % 2 === 0);
console.log(`pares=${pares.join("-")}`);
