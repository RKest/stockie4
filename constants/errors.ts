import actions from "./actions.ts";

export default {
    NO_DATASETS_NUMBER: "Provide number of training datasets (5_us_txt_@${ NUMBER HERE })",
    UNIMPLEMENTED: "Unimplemented",
    NO_ACTION: `Provide a valid action (one of ${actions})`
} as const;