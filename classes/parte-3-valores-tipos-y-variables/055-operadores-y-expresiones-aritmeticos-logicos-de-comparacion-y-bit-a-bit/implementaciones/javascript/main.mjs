import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${a + b} resta=${a - b} mult=${a * b} div=${Math.trunc(a / b)} mod=${a % b}`);
