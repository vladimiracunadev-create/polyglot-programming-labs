import { readFileSync } from "node:fs";

const suma = (a, b) => a + b;
const producto = (a, b) => a * b;
const aplicar = (f, a, b) => f(a, b);

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`suma=${aplicar(suma, a, b)} producto=${aplicar(producto, a, b)}`);
