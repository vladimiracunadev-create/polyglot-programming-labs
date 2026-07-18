import { readFileSync } from "node:fs";

const w: string = readFileSync(0, "utf8").trim();
const valido = /^[a-z]+$/.test(w);
console.log(`valido=${valido ? "true" : "false"}`);
