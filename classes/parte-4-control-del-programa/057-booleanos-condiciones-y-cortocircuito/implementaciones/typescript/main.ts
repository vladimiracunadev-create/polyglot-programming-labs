import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const tf = (x: boolean): string => (x ? "true" : "false");
const pos: boolean = n > 0;
const par: boolean = n % 2 === 0;
console.log(`positivo=${tf(pos)} par=${tf(par)} ambos=${tf(pos && par)}`);
