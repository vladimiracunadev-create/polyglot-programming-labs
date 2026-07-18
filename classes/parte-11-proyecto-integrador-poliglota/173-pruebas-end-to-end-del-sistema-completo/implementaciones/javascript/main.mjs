import { readFileSync } from "node:fs";

const [a, b, esperado] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`e2e=${a + b === esperado ? "pasa" : "falla"}`);
