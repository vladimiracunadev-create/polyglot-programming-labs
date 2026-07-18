import { readFileSync } from "node:fs";

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
const viejo = n * 2, nuevo = n + n;
console.log(`equivalente=${viejo === nuevo ? "true" : "false"} resultado=${nuevo}`);
