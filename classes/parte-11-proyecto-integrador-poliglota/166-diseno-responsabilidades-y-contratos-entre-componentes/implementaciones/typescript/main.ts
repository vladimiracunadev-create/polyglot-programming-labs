import { readFileSync } from "node:fs";

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`contrato=${a === b ? "compatible" : "incompatible"}`);
