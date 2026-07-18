import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let valor: number;
{
  const recurso = { valor: n };
  valor = recurso.valor;
}
console.log(`valor=${valor} estado=liberado`);
