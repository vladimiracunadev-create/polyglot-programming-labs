import { readFileSync } from "node:fs";

async function doble(x) {
  return x * 2;
}

const n = parseInt(readFileSync(0, "utf8").trim(), 10);
(async () => {
  const resultado = await doble(n);
  console.log(`resultado=${resultado}`);
})();
