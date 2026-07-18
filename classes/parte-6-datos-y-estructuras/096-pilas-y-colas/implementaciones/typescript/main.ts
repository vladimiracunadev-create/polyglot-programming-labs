import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const pila = [...nums].reverse().join("-");
const cola = nums.join("-");
console.log(`pila=${pila} cola=${cola}`);
