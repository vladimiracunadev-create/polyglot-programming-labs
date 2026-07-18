import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const mx = a > b ? a : b;
console.log(`max=${mx}`);
