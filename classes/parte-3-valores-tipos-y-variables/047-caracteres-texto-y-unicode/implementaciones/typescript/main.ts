import { readFileSync } from "node:fs";

const data: string = readFileSync(0, "utf8");
const c: string = data[0];
console.log(`char=${c} codigo=${data.charCodeAt(0)}`);
