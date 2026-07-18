import { readFileSync } from "node:fs";

const doble = (x) => x * 2;
const wrapper = (x) => `wrap(${doble(x)})`;

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`envuelto=${wrapper(n)}`);
