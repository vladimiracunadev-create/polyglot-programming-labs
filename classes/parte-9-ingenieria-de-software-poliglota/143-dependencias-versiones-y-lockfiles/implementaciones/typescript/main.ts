import { readFileSync } from "node:fs";

const [mayor, menor, parche] = readFileSync(0, "utf8").trim().split(".").map(Number);
console.log(`mayor=${mayor} menor=${menor} parche=${parche}`);
