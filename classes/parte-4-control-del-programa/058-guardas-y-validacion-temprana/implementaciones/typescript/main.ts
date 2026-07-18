import { readFileSync } from "node:fs";

const edad: number = parseInt(readFileSync(0, "utf8").trim(), 10);
if (edad < 0) console.log("invalido");
else if (edad < 18) console.log("menor");
else console.log("adulto");
