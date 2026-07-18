import { readFileSync } from "node:fs";

const w: string = readFileSync(0, "utf8").trim();
console.log(`invertido=${[...w].reverse().join("")}`);
