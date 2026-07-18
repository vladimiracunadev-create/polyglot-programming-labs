import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const resultado: number = a + b;
console.log(`resultado=${resultado}`);
