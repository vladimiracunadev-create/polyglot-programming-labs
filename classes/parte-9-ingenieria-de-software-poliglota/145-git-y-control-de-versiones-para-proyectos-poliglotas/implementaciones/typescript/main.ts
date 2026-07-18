import { readFileSync } from "node:fs";

const msgs: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`commits=${msgs.length}`);
