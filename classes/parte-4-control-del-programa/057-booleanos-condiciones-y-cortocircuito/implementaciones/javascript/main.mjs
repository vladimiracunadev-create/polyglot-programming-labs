import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const tf = (x) => (x ? "true" : "false");
const pos = n > 0;
const par = n % 2 === 0;
console.log(`positivo=${tf(pos)} par=${tf(par)} ambos=${tf(pos && par)}`);
