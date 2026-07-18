import { readFileSync } from "node:fs";

const doblar = (x: number): number => x * 2;
const incrementar = (x: number): number => x + 1;
const compuesta = (x: number): number => incrementar(doblar(x));

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${compuesta(n)}`);
