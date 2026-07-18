import { readFileSync } from "node:fs";

namespace matematicas {
  export function doble(n: number): number {
    return 2 * n;
  }
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
console.log(`resultado=${matematicas.doble(n)}`);
