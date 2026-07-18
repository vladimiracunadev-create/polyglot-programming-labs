import { readFileSync } from "node:fs";

const t: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
const nombre: string = t[0];
const edad: number = parseInt(t[1], 10);
console.log(`{"nombre": "${nombre}", "edad": ${edad}}`);
