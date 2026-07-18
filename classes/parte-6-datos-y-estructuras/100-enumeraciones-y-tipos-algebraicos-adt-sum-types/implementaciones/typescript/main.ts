import { readFileSync } from "node:fs";

const t: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
let area: number;
if (t[0] === "cuadrado") area = Number(t[1]) ** 2;
else area = Number(t[1]) * Number(t[2]);
console.log(`area=${area}`);
