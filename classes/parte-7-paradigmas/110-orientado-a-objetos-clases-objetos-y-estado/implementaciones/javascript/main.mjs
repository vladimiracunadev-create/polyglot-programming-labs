import { readFileSync } from "node:fs";

class Contador {
  constructor() {
    this.cuenta = 0;
  }
  incrementar() {
    this.cuenta++;
  }
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const c = new Contador();
for (let i = 0; i < n; i++) c.incrementar();
console.log(`cuenta=${c.cuenta}`);
