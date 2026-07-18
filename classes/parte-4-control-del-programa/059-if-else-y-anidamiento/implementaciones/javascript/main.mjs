import { readFileSync } from "node:fs";

const score = parseInt(readFileSync(0, "utf8").trim(), 10);
let nota;
if (score >= 90) nota = "A";
else if (score >= 80) nota = "B";
else if (score >= 70) nota = "C";
else nota = "F";
console.log(`nota=${nota}`);
