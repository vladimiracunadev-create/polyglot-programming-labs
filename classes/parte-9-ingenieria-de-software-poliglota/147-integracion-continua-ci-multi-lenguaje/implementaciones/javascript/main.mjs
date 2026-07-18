import { readFileSync } from "node:fs";

const pasos = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(`ci=${pasos.every((p) => p === 1) ? "verde" : "rojo"}`);
