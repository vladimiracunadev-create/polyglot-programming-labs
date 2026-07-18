import { readFileSync } from "node:fs";

interface Animal { sonido(): string; }
class Perro implements Animal { sonido() { return "guau"; } }
class Gato implements Animal { sonido() { return "miau"; } }
class Vaca implements Animal { sonido() { return "muu"; } }

const tipo: string = readFileSync(0, "utf8").trim();
const animales: Record<string, Animal> = { perro: new Perro(), gato: new Gato(), vaca: new Vaca() };
console.log(`sonido=${animales[tipo].sonido()}`);
