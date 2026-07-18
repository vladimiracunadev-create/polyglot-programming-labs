import { readFileSync } from "node:fs";

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
try {
  if (b === 0) throw new Error("div");
  console.log(`resultado=${Math.trunc(a / b)}`);
} catch {
  console.log("error=division por cero");
}
