import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(n === 0 ? "valor=ausente" : `valor=${n}`);
