import { readFileSync } from "node:fs";

const doble = (x: number): number => x * 2;
const wrapper = (x: number): string => `wrap(${doble(x)})`;

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`envuelto=${wrapper(n)}`);
