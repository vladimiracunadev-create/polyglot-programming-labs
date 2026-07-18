import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
for (let i = 0; i < n; i++) {
  const tmp = {}; // sin referencia persistente, será recolectado
  void tmp;
}
console.log(`creados=${n} estado=recolectado`);
