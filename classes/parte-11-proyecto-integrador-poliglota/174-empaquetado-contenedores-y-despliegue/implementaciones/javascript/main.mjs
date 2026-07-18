import { readFileSync } from "node:fs";

const version = readFileSync(0, "utf8").trim();
console.log(`imagen=app:${version}`);
