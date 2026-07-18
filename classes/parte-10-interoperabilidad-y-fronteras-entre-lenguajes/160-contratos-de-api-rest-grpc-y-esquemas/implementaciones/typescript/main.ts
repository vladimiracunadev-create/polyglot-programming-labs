import { readFileSync } from "node:fs";

const [metodo, recurso] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`contrato=${metodo} /${recurso}`);
