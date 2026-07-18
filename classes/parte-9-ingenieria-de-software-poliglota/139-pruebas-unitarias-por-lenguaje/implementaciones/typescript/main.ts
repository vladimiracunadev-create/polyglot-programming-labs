import { readFileSync } from "node:fs";

const [a, b, esperado] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`test=${a + b === esperado ? "pasa" : "falla"}`);
