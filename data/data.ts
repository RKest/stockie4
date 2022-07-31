import * as std from "https://deno.land/std@0.148.0/path/mod.ts";
import { io } from "../functional/io.ts";
import JsonFileWriter, { IJsonFileWriter } from "../functional/large-json-writer.ts";
import { groupArray } from "../functional/miscellaneous.ts";

export { Parser, PathFinder };

const __dirname = new URL(".", import.meta.url).pathname;
const N_TEST_SYMBOLS = 50;
const trainPath = __dirname + "_txtData.json";
const testPath = __dirname + "_txtTestData.json";

class PathFinder {
  private paths: string[] = [];
  private ROOT_DIR: string = __dirname;

  /**
   * Top level traversion
   * Returns all files recuresevely in a directory
   */

  public async collect(noDirs: number) {
    for (let i = 0; i < noDirs; i++) {
      await this.traverse(this.template(i));
    }
    if (!this.paths.length) {
      Deno.exit(1);
    }
    return this.paths;
  }

  private template(num: number): string {
    return `${this.ROOT_DIR}/5_us_txt_@${num}`;
  }

  private async traverse(dir: string) {
    const dirsOrFiles = Deno.readDir(dir);
    for await (const dirOfFile of dirsOrFiles) {
      const resolvedDirOrFile = std.resolve(dir, dirOfFile.name);
      const fileOrDirStat = await Deno.stat(resolvedDirOrFile);
      if (fileOrDirStat && fileOrDirStat.isDirectory) {
        await this.traverse(resolvedDirOrFile);
      } else if (fileOrDirStat) {
        this.paths.push(resolvedDirOrFile);
      }
    }

    return this.paths;
  }
}

class Parser {
  private trainJsonWriter = new JsonFileWriter(trainPath, { doStrip: true });
  private testJsonWriter = new JsonFileWriter(testPath, { doStrip: true });
  private testData: number[][] = [];

  public get testPath() {
    return testPath;
  }

  public get trainPath() {
    return trainPath;
  }
  /**
   * Takes a path of a txt file and returns price array
   */
  public async parse(pathArr: string[]) {
    if (!this.isParsingNescessery()) {
      return;
    }
    const pathGroups = groupArray(pathArr);
    const nGroups = pathGroups.length;
    const nTestInterval = Math.round(N_TEST_SYMBOLS / nGroups);

    for (let i = 0; i < nGroups; i++) {
      const pathGroup = pathGroups[i];
      const fileStrings = await Promise.all(pathGroup.map(io.read));
      const openPrices = fileStrings.map((fileString) =>
        fileString.split("\n").slice(1, -1).map((line) =>
          Number(line.split(",")[4])
        )
      );
      const validOpenPrices = openPrices.filter((openPricesArray) =>
        openPricesArray.length > 50
      );
      await this.write(validOpenPrices, nGroups, i, nTestInterval);

      console.log(`Parsing ${i + 1} / ${nGroups}`);
    }
    await io.writeJson(this.testPath, this.testData);
    console.log("Parsed");
  }

  public async write(
    prices: number[][],
    nGroups: number,
    i: number,
    interval: number,
    testWriter: IJsonFileWriter = this.testJsonWriter,
    trainWriter: IJsonFileWriter = this.trainJsonWriter,
  ) {
    if (i % interval == 0) {
      const isNextGroupTrain = (i + 1) % interval != 0;
      const closing = i + interval >= nGroups || (isNextGroupTrain && i + 2 >= nGroups);
      await testWriter.writeArray(prices, closing);
    } else {
      const isNextGroupTest = (i + 1) % interval == 0;
      const closing = i + 1 >= nGroups || (isNextGroupTest && i + 2 >= nGroups);
      await trainWriter.writeArray(prices, closing);
    }
  }

  public async cleanup() {
    await io.remove(trainPath);
    await io.remove(testPath);
  }

  private async isParsingNescessery() {
    return !await io.exists(this.testPath);
  }
}
