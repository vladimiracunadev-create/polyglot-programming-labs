import { readFileSync } from "node:fs";

const c: string[] = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`componentes=${c.length} nombres=${c.join("-")}`);
