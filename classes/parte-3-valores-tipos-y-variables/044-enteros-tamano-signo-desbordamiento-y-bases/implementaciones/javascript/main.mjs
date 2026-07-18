import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`dec=${n} hex=${n.toString(16)} oct=${n.toString(8)} bin=${n.toString(2)}`);
