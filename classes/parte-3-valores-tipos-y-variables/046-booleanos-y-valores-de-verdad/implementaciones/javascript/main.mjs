import { readFileSync } from "node:fs";

const [ai, bi] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const a = ai !== 0;
const b = bi !== 0;
const tf = (x) => (x ? "true" : "false");
console.log(`and=${tf(a && b)} or=${tf(a || b)} not_a=${tf(!a)}`);
