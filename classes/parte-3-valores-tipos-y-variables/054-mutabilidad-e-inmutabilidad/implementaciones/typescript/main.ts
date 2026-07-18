import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const parts: number[] = [];
for (let i = 1; i <= n; i++) parts.push(i);
console.log(`sec=${parts.join("-")}`);
