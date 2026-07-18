import { readFileSync } from "node:fs";

let [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);

// Desestructuración: intercambio en una sola línea.
[a, b] = [b, a];

console.log(`a=${a} b=${b}`);
