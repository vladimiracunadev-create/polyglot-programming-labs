import { readFileSync } from "node:fs";

const nums: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const copia: number[] = [...nums];
copia[copia.length - 1] = 99;
console.log(`original=${nums.join("-")} copia=${copia.join("-")}`);
