import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
// El anfitrion evalua el script embebido con los datos.
const resultado = a + b;
console.log(`resultado=${resultado}`);
