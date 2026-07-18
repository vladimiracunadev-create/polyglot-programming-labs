import { readFileSync } from "node:fs";

let [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);

[a, b] = [b, a];

console.log(`a=${a} b=${b}`);
