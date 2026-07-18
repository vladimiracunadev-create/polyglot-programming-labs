import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const signo = n > 0 ? "positivo" : n < 0 ? "negativo" : "cero";
console.log(`signo=${signo}`);
