import { readFileSync } from "node:fs";

const c = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`componentes=${c.length} nombres=${c.join("-")}`);
