import { readFileSync } from "node:fs";

function doblar(caja: { v: number }): void {
  caja.v *= 2;
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const antes: number = n;
const caja = { v: n };
doblar(caja);
console.log(`antes=${antes} despues=${caja.v}`);
