import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
let valor;
{
  const recurso = { valor: n };
  valor = recurso.valor;
  // en JS el GC libera; aquí el ámbito marca el fin de uso
}
console.log(`valor=${valor} estado=liberado`);
