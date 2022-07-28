type PossibleActions = typeof import("../constants/actions.ts")["default"][number];
type ActionFunctions = { [Action in PossibleActions]: () => void };