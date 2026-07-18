import { readFileSync } from "node:fs";

type Res = { ok: number } | { err: string };

function dividir(a: number, b: number): Res {
  if (b === 0) return { err: "division" };
  return { ok: Math.trunc(a / b) };
}

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
const r = dividir(a, b);
console.log("err" in r ? `err=${r.err}` : `ok=${r.ok}`);
