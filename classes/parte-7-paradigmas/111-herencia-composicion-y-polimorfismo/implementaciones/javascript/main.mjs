import { readFileSync } from "node:fs";

class Perro { sonido() { return "guau"; } }
class Gato { sonido() { return "miau"; } }
class Vaca { sonido() { return "muu"; } }

const tipo = readFileSync(0, "utf8").trim();
const animales = { perro: new Perro(), gato: new Gato(), vaca: new Vaca() };
console.log(`sonido=${animales[tipo].sonido()}`);
