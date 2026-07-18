import { readFileSync } from "node:fs";

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
const x: number = n;
{
  const x: number = n + 10;
  console.log(`interno=${x} externo=${n}`);
}
