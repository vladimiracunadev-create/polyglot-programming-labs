import { readFileSync } from "node:fs";

class Cuenta {
  private saldoInterno = 0;
  depositar(monto: number): void {
    this.saldoInterno += monto;
  }
  saldo(): number {
    return this.saldoInterno;
  }
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const c = new Cuenta();
c.depositar(n);
c.depositar(n);
console.log(`saldo=${c.saldo()}`);
