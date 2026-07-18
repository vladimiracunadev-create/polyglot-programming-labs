import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
// Objeto literal con método (modelo de prototipos).
const obj = {
  valor: n,
  doble() {
    return this.valor * 2;
  },
};
console.log(`resultado=${obj.doble()}`);
