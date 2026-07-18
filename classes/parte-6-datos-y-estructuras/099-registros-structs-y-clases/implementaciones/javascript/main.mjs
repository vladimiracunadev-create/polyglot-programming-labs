import { readFileSync } from "node:fs";

const t = readFileSync(0, "utf8").trim().split(/\s+/);
const persona = { nombre: t[0], edad: parseInt(t[1], 10) };
console.log(`Persona(nombre=${persona.nombre}, edad=${persona.edad})`);
