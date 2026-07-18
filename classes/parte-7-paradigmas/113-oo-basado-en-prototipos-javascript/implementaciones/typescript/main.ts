import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const obj = {
  valor: n,
  doble(): number {
    return this.valor * 2;
  },
};
console.log(`resultado=${obj.doble()}`);
