import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
for (let i = 0; i < n; i++) {
  const tmp: Record<string, unknown> = {};
  void tmp;
}
console.log(`creados=${n} estado=recolectado`);
