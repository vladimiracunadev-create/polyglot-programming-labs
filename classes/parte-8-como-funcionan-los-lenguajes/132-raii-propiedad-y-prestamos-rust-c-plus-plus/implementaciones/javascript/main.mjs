import { readFileSync } from "node:fs";

const doble = (x) => x * 2;
const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${doble(n)}`);
