import { readFileSync } from "node:fs";

type Op = (a: number, b: number) => number;
const suma: Op = (a, b) => a + b;
const producto: Op = (a, b) => a * b;
const aplicar = (f: Op, a: number, b: number): number => f(a, b);

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${aplicar(suma, a, b)} producto=${aplicar(producto, a, b)}`);
