import { Parser, PathFinder } from "./data.ts";

export default async (nDataDirs: number) => {
  const pathFinder = new PathFinder();
  const parser = new Parser();

  const paths = await pathFinder.collect(nDataDirs);
  
  await parser.parse(paths);

  const process = Deno.run({ cmd: ["python3", "ai/data_save.py"] });
  const status = await process.status();

  if (status.code === 0) {
    parser.cleanup();
  }
};
