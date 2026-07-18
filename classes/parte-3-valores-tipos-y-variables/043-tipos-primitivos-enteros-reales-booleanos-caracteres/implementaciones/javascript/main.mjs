import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const par = n % 2 === 0 ? "true" : "false";
console.log(`entero=${n} real=${n.toFixed(1)} par=${par}`);
