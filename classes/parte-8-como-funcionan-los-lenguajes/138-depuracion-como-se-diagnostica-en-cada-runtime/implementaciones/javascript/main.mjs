import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`valor=${n} cuadrado=${n * n} cubo=${n * n * n}`);
