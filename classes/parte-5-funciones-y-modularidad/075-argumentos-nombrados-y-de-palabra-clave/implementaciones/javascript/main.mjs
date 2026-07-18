import { readFileSync } from "node:fs";

// JS simula argumentos nombrados con un objeto.
function punto({ x, y }) {
  return `punto(x=${x}, y=${y})`;
}

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(punto({ x: a, y: b }));
