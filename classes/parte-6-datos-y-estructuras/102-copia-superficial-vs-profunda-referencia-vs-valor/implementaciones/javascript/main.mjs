import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const copia = [...nums];
copia[copia.length - 1] = 99;
console.log(`original=${nums.join("-")} copia=${copia.join("-")}`);
