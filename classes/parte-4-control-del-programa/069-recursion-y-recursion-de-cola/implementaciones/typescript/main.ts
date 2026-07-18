import { readFileSync } from "node:fs";

function fib(n: number): number {
  return n < 2 ? n : fib(n - 1) + fib(n - 2);
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`fib=${fib(n)}`);
