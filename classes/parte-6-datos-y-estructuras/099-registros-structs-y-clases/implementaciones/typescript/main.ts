import { readFileSync } from "node:fs";

interface Persona {
  nombre: string;
  edad: number;
}

const t: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
const p: Persona = { nombre: t[0], edad: parseInt(t[1], 10) };
console.log(`Persona(nombre=${p.nombre}, edad=${p.edad})`);
