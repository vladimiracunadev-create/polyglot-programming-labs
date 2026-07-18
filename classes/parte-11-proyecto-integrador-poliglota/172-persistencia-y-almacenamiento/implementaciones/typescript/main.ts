import { readFileSync } from "node:fs";

const [clave, valor] = readFileSync(0, "utf8").trim().split(/\s+/);
const almacen = new Map<string, string>();
almacen.set(clave, valor);
console.log(`guardado=${clave}=${almacen.get(clave)}`);
