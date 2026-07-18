import { readFileSync } from "node:fs";

const d: number = parseInt(readFileSync(0, "utf8").trim(), 10);
let dia: string;
switch (d) {
  case 1: dia = "lunes"; break;
  case 2: dia = "martes"; break;
  case 3: dia = "miercoles"; break;
  case 4: dia = "jueves"; break;
  case 5: dia = "viernes"; break;
  case 6: dia = "sabado"; break;
  case 7: dia = "domingo"; break;
  default: dia = "invalido";
}
console.log(`dia=${dia}`);
