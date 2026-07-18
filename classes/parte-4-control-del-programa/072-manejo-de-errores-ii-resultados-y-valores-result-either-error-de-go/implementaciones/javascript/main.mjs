import { readFileSync } from "node:fs";

function dividir(a, b) {
  if (b === 0) return { err: "division" };
  return { ok: Math.trunc(a / b) };
}

const [a, b] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const r = dividir(a, b);
console.log(r.err ? `err=${r.err}` : `ok=${r.ok}`);
