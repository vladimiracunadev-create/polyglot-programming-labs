import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const arr = new Array(n);
for (let i = 0; i < n; i++) arr[i] = i + 1;
console.log(`reservado=${n} suma=${arr.reduce((a, b) => a + b, 0)}`);
