import { readFileSync } from "node:fs";

const [x, y] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`equivalente=${x === y ? "true" : "false"}`);
