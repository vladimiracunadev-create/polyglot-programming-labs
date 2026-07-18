import { readFileSync } from "node:fs";

function punto({ x, y }: { x: number; y: number }): string {
  return `punto(x=${x}, y=${y})`;
}

const [a, b]: number[] = readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
console.log(punto({ x: a, y: b }));
