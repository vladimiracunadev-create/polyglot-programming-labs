import { readFileSync } from "node:fs";

const s: string = readFileSync(0, "utf8").trim();
const longitud: number = s.length;
console.log(`movido=${s} longitud=${longitud}`);
