import { readFileSync } from "node:fs";

const version = readFileSync(0, "utf8").trim();
console.log(`desplegado=v${version}`);
