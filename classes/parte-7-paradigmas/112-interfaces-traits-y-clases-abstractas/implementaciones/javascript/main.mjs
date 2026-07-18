import { readFileSync } from "node:fs";

class Cuadrado { constructor(l) { this.l = l; } area() { return this.l * this.l; } }
class Rectangulo { constructor(a, b) { this.a = a; this.b = b; } area() { return this.a * this.b; } }

const t = readFileSync(0, "utf8").trim().split(/\s+/);
const f = t[0] === "cuadrado" ? new Cuadrado(Number(t[1])) : new Rectangulo(Number(t[1]), Number(t[2]));
console.log(`area=${f.area()}`);
