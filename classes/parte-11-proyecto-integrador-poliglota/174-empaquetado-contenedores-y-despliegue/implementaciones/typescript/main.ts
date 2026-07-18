import { readFileSync } from "node:fs";

const version: string = readFileSync(0, "utf8").trim();
console.log(`imagen=app:${version}`);
