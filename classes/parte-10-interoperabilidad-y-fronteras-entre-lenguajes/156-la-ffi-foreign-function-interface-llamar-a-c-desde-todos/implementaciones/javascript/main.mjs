import { readFileSync } from "node:fs";

const doble = (x) => x * 2; // función 'externa' vía FFI
const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${doble(n)}`);
