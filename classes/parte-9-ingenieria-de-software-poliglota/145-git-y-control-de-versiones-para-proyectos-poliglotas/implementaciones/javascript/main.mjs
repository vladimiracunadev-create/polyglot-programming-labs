import { readFileSync } from "node:fs";

const msgs = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`commits=${msgs.length}`);
