import { readFileSync } from "node:fs";

const s = readFileSync(0, "utf8").trim();
const longitud = s.length; // JS usa GC: la cadena sigue disponible.
console.log(`movido=${s} longitud=${longitud}`);
