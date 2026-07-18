import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`divisor=${b % a === 0 ? "true" : "false"}`);
