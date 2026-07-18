import { readFileSync } from "node:fs";

class Cuenta {
  #saldo = 0; // campo privado real
  depositar(monto) {
    this.#saldo += monto;
  }
  saldo() {
    return this.#saldo;
  }
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const c = new Cuenta();
c.depositar(n);
c.depositar(n);
console.log(`saldo=${c.saldo()}`);
