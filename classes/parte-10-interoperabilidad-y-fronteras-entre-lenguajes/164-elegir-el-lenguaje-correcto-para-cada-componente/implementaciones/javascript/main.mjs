import { readFileSync } from "node:fs";

const tipo = readFileSync(0, "utf8").trim();
const rec = { sistemas: "Rust", web: "TypeScript", datos: "SQL" };
console.log(`lenguaje=${rec[tipo] ?? "Python"}`);
