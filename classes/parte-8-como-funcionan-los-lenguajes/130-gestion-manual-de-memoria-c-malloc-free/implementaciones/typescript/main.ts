import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const arr: number[] = new Array(n);
for (let i = 0; i < n; i++) arr[i] = i + 1;
console.log(`reservado=${n} suma=${arr.reduce((a, b) => a + b, 0)}`);
