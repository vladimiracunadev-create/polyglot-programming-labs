import { readFileSync } from "node:fs";

const data = readFileSync(0, "utf8");
const c = data[0];
console.log(`char=${c} codigo=${data.charCodeAt(0)}`);
