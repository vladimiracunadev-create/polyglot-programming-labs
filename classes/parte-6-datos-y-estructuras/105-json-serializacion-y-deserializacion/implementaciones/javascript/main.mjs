import { readFileSync } from "node:fs";

const t = readFileSync(0, "utf8").trim().split(/\s+/);
const nombre = t[0];
const edad = parseInt(t[1], 10);
console.log(`{"nombre": "${nombre}", "edad": ${edad}}`);
