import { readFileSync } from "node:fs";

const linea = readFileSync(0, "utf8").replace(/\r?\n$/, "");
const palabras = linea.split(/\s+/).filter((w) => w.length > 0).length;
console.log(`palabras=${palabras} caracteres=${linea.length}`);
