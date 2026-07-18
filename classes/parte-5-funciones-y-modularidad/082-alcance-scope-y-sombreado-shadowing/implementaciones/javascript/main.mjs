import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const x = n;
{
  const x = n + 10; // sombrea a la externa dentro del bloque
  console.log(`interno=${x} externo=${n}`);
}
