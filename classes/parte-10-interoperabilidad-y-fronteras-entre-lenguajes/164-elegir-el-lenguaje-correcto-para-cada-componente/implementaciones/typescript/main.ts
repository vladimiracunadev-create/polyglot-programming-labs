import { readFileSync } from "node:fs";

const tipo: string = readFileSync(0, "utf8").trim();
const rec: Record<string, string> = { sistemas: "Rust", web: "TypeScript", datos: "SQL" };
console.log(`lenguaje=${rec[tipo] ?? "Python"}`);
