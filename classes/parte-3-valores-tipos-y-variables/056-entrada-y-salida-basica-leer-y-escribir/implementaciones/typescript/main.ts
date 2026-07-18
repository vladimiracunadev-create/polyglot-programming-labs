import { readFileSync } from "node:fs";

const linea: string = readFileSync(0, "utf8").replace(/\r?\n$/, "");
console.log(`eco: ${linea}`);
