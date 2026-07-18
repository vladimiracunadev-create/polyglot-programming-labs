import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const opcion: number | null = n > 0 ? n : null;
console.log(opcion !== null ? `resultado=${opcion * 2}` : "resultado=nada");
