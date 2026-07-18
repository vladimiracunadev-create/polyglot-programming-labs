import { readFileSync } from "node:fs";

const doblar = (x) => x * 2;
const incrementar = (x) => x + 1;
const compuesta = (x) => incrementar(doblar(x));

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${compuesta(n)}`);
