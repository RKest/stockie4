import { opine, serveStatic } from "https://deno.land/x/opine@2.0.0/mod.ts";
import { __rootDir } from "../app.ts";
import { io } from "../functional/io.ts";
import { avgerageArray } from "../functional/miscellaneous.ts";

const DATA_POINTS_AMOUNT = 150;
const N_MODEL_GROUPS = 4;
const INFORMATION_OFFSET = 3;

export default () => {
  const app = opine();
  app.use(serveStatic("client"));

  app.get("/chartData", async (req, res) => {
    const netNum = req.query.netNum;
    const modelDataString: string = await io.read(
      `${__rootDir}/models/slope-model-${netNum}.log`,
    );
    const modelGropus: number[][] = Array.from(Array(N_MODEL_GROUPS), () => []);

    const modelData = modelDataString.split("\n");
    const modelVariables = modelData.map((str) => str.split(","));
    const modelIncrement = Math.floor(
      modelVariables.length / DATA_POINTS_AMOUNT,
    );

    for (let i = 0; i < modelVariables[0].length - INFORMATION_OFFSET; i++) {
      for (let j = 0; j < modelVariables.length; j += modelIncrement) {
        const modelSlice = modelVariables.slice(j, j + modelIncrement);
        const modelValues = modelSlice.map((el) => el[i + INFORMATION_OFFSET]);
        const sliceAverage = avgerageArray(modelValues.map(Number));
        modelGropus[i].push(sliceAverage);
      }
    }

    res.json(modelGropus);
  });

  app.listen(8080, () => console.log("http://localhost:8080"));
};
