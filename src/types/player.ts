import { State } from "../enums/state.ts";

export type Player = {
    id: string,
    is_left: boolean,
    stack: bigint,
    behind: bigint,
    front: bigint,
    round_bet: bigint,
    state: State
}
