import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const t = [b, a];
console.log(`tupla=(${t[0]}, ${t[1]})`);
