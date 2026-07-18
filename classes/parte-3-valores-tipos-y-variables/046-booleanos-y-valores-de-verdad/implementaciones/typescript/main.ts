import { readFileSync } from "node:fs";

const [ai, bi]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const a: boolean = ai !== 0;
const b: boolean = bi !== 0;
const tf = (x: boolean): string => (x ? "true" : "false");
console.log(`and=${tf(a && b)} or=${tf(a || b)} not_a=${tf(!a)}`);
