import { readFileSync } from "node:fs";

const doble = (x: number): number => x * 2;
const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${doble(n)}`);
