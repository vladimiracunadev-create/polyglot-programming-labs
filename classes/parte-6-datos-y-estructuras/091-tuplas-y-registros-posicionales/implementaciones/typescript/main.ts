import { readFileSync } from "node:fs";

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const t: [number, number] = [b, a];
console.log(`tupla=(${t[0]}, ${t[1]})`);
