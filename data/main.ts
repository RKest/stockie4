import { io } from "../functional/io.ts";
import { Organiser, Parser, PathFinder } from "./data.ts";

export default async (nDataDirs: number) => {
  const pathFinder = new PathFinder();
  const organiser = new Organiser();
  const parser = new Parser();

  const paths = await pathFinder.collect(nDataDirs);

  if (!paths.length) {
    Deno.exit(1);
  }

  if (!await io.exists(parser.trainPath)) {
    await parser.parse(paths);
    console.log("Parsed");
    // await parser.save();
    // console.log("Saved");
    await organiser.transfer();
    console.log("Transfered");
  }

  const process = Deno.run({ cmd: ["python3", "ai/data_save.py"] });
  const status = await process.status();

  if (status.code === 0) {
    parser.cleanup();
  }
};
