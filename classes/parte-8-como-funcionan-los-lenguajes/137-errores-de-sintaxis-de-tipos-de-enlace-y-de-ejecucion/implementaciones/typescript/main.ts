import { readFileSync } from "node:fs";

const codigo: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const nombres: Record<number, string> = { 1: "sintaxis", 2: "tipos", 3: "enlace", 4: "ejecucion" };
console.log(`error=${nombres[codigo] ?? "desconocido"}`);
