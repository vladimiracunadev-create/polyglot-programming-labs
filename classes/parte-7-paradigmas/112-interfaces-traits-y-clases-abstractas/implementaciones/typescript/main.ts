import { readFileSync } from "node:fs";

interface Forma { area(): number; }
class Cuadrado implements Forma { constructor(private l: number) {} area() { return this.l * this.l; } }
class Rectangulo implements Forma { constructor(private a: number, private b: number) {} area() { return this.a * this.b; } }

const t: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
const f: Forma = t[0] === "cuadrado" ? new Cuadrado(Number(t[1])) : new Rectangulo(Number(t[1]), Number(t[2]));
console.log(`area=${f.area()}`);
