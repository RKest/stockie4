import { io } from "../functional/io.ts";
import { assert } from "https://deno.land/std@0.149.0/testing/asserts.ts";

const res = await io.exists("app.ts");
const resabs = await io.exists(
  "/home/max/Documents/Projs/stockie4/app.ts",
);
const resnot = await io.exists("NOT_EXISTANT.ts");

Deno.test("io exists", () => assert(res));
Deno.test("io exists abs", () => assert(resabs));
Deno.test("io doesn't exist", () => assert(!resnot));
