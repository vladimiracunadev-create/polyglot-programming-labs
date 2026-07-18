import { readFileSync } from "node:fs";

function doblar(caja) {
  caja.v *= 2;
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const antes = n;
const caja = { v: n };
doblar(caja);
console.log(`antes=${antes} despues=${caja.v}`);
