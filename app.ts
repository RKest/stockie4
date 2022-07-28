import prepData from "./data/main.ts";
import err from "./constants/errors.ts";
import {} from "./types/args.d.ts";
import runRouter from "./router/main.ts";

export const __rootDir = new URL(".", import.meta.url).pathname;

const action = Deno.args[0] as PossibleActions;
const actions: ActionFunctions = {
  prep: () => {
    const nTrainingDatasets = +Deno.args[1];
    if (!nTrainingDatasets || Number.isNaN(nTrainingDatasets)) {
      throw new Error(err.NO_DATASETS_NUMBER);
    }
    prepData(nTrainingDatasets);
  },
  train: async () => {
    const process = Deno.run({ cmd: ["python3", "ai/main.py"] });
    const status = await process.status();
    console.log(status);
  },
  run: () => {
    throw new Error(err.UNIMPLEMENTED);
  },
  show: () => {
    runRouter();
  },
  quit: () => {},
};

if (action in actions) {
  actions[action]();
} else {
  throw err.NO_ACTION;
}
