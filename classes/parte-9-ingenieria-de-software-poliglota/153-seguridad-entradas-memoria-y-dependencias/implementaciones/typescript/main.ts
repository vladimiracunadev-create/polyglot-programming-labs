import { readFileSync } from "node:fs";

const w: string = readFileSync(0, "utf8").trim();
const seguro = /^[A-Za-z0-9]+$/.test(w);
console.log(`seguro=${seguro ? "true" : "false"}`);
