// import { resolve } from "path";

import * as std from "https://deno.land/std@0.148.0/path/mod.ts";
import { io } from "../functional/io.ts";
export { Organiser, Parser, PathFinder };

const __dirname = new URL(".", import.meta.url).pathname;
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
      await this.traverse(this.template(i))
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
  private jsonData: number[][] = [];

  public get trainPath() { return trainPath; }
  /**
   * Takes a path of a txt file and returns price array
   */
  public async parse(pathArr: string[]) {
    const arrLen = pathArr.length;
    this.append('[');
    for (let i = 0; i < pathArr.length; i += 100) {
      const paths = pathArr.slice(i, i + 100);
      const fileStrings = await Promise.all( paths.map(io.read) );
      for (const fileString of fileStrings){
        const openPrices = fileString.split("\n").slice(1, -1).map((line) =>
          Number(line.split(",")[4])
        );
        if (openPrices.length > 50) {
          this.output(openPrices);
        }
      }
      this.append(JSON.stringify(this.jsonData));
      this.append(',');
      this.empty();
      console.log(`Parsing ${i}/${arrLen}`);
    }
    this.append("]")
    console.log("Saved")
  }

  /**
   * Save the accumulated data
   */
  // public async save() {
  //   await io.writeJson(trainPath, this.jsonData);
  //   console.log("saved");
  // }

  public async cleanup() {
    await io.remove(trainPath);
    await io.remove(testPath);
  }

  private append = async (data: string) => await io.append(trainPath, data);

  private empty() {
    this.jsonData = [];
  }

  private output(array: number[]) {
    this.jsonData.push(array);
  }

}

class Organiser {
  /**
   * Transfers some of the data from train data to be used for test data
   */
  public async transfer(amountOfSymbols = 50) {
    const trainData = await io.readJson<number[][]>(trainPath);
    const testData: number[][] = [];
    for (let i = 0; i < amountOfSymbols; i++) {
      const r = Math.floor(Math.random() * trainData.length);
      const dataToTransfer = trainData.splice(r, 1);
      testData.push(dataToTransfer[0]);
    }

    await Promise.all([
      io.writeJson(trainPath, trainData),
      io.writeJson(testPath, testData)
    ]);

    console.log("Done");
  }
}
