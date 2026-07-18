import { readFileSync } from "node:fs";

function fib(n) {
  return n < 2 ? n : fib(n - 1) + fib(n - 2);
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`fib=${fib(n)}`);
