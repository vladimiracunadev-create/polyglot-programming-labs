import { readFileSync } from "node:fs";

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const mx: number = a > b ? a : b;
console.log(`max=${mx}`);
