import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const aristas = Math.floor(nums.length / 2);
const nodos = new Set(nums).size;
console.log(`aristas=${aristas} nodos=${nodos}`);
