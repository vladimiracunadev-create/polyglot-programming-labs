import { readFileSync } from "node:fs";

// Números en JS: un solo tipo `number` (doble de 64 bits) para todo.
const [precio, cantidad, descuento] = readFileSync(0, "utf8")
  .trim()
  .split(/\s+/)
  .map(Number);

const subtotal = precio * cantidad;
const total = subtotal * (1 - descuento);

console.log(`Total: ${total.toFixed(2)}`);
