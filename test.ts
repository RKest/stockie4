import { io } from "./functional/io.ts";

const str = await io.read("./data/_txtData.json");
console.log(str.slice(764461, 764472));