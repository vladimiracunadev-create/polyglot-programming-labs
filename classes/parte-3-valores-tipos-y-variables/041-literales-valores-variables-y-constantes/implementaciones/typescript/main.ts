import { readFileSync } from "node:fs";

// TypeScript añade tipos estáticos sobre JavaScript: se comprueban al compilar.
const [precio, cantidad, descuento]: number[] = readFileSync(0, "utf8")
  .trim()
  .split(/\s+/)
  .map(Number);

const subtotal: number = precio * cantidad;
const total: number = subtotal * (1 - descuento);

console.log(`Total: ${total.toFixed(2)}`);
