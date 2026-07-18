import { readFileSync } from "node:fs";

const nums = readFileSync(0, "utf8").trim().split(/\s+/);
console.log(`csv=${nums.join(",")} campos=${nums.length}`);
