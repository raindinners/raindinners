import { StartState } from "../enums/startState.ts";

export type Start = {
    state: StartState,
    time: number | null | undefined
}
