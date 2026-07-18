import { readFileSync } from "node:fs";

const [clave, valor] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`serializado=${clave}:${valor}`);
