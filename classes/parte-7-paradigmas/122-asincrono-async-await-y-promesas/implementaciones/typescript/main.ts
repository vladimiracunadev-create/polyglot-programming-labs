import { readFileSync } from "node:fs";

async function doble(x: number): Promise<number> {
  return x * 2;
}

const n: number = parseInt(readFileSync(0, "utf8").trim(), 10);
(async () => {
  const resultado: number = await doble(n);
  console.log(`resultado=${resultado}`);
})();
