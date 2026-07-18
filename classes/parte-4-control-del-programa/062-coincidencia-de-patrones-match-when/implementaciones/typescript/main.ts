import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const signo: string = n > 0 ? "positivo" : n < 0 ? "negativo" : "cero";
console.log(`signo=${signo}`);
